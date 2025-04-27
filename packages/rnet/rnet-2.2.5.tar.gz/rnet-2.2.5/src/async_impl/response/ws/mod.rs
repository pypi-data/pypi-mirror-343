mod message;

use crate::{
    error::Error,
    typing::{Cookie, HeaderMap, SocketAddr, StatusCode, Version},
};
use bytes::Bytes;
use futures_util::{
    SinkExt, StreamExt, TryStreamExt,
    stream::{SplitSink, SplitStream},
};
pub use message::Message;
use pyo3::{IntoPyObjectExt, prelude::*, pybacked::PyBackedStr};
use pyo3_async_runtimes::tokio::future_into_py;
#[cfg(feature = "docs")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};
use rquest::{
    Utf8Bytes,
    header::{self, HeaderValue},
};
use std::sync::Arc;
use tokio::sync::Mutex;

type Sender = Arc<Mutex<Option<SplitSink<rquest::WebSocket, rquest::Message>>>>;
type Receiver = Arc<Mutex<Option<SplitStream<rquest::WebSocket>>>>;

/// A WebSocket response.
#[cfg_attr(feature = "docs", gen_stub_pyclass)]
#[pyclass]
pub struct WebSocket {
    version: Version,
    status_code: StatusCode,
    remote_addr: Option<SocketAddr>,
    headers: header::HeaderMap,
    protocol: Option<HeaderValue>,
    sender: Sender,
    receiver: Receiver,
}

impl WebSocket {
    pub async fn new(builder: rquest::WebSocketRequestBuilder) -> Result<WebSocket, rquest::Error> {
        let response = builder.send().await?;

        let version = Version::from_ffi(response.version());
        let status_code = StatusCode::from(response.status());
        let remote_addr = response.remote_addr().map(SocketAddr::from);
        let headers = response.headers().clone();
        let websocket = response.into_websocket().await?;
        let protocol = websocket.protocol().cloned();
        let (sender, receiver) = websocket.split();

        Ok(WebSocket {
            version,
            status_code,
            remote_addr,
            headers,
            protocol,
            sender: Arc::new(Mutex::new(Some(sender))),
            receiver: Arc::new(Mutex::new(Some(receiver))),
        })
    }

    #[inline(always)]
    pub fn sender(&self) -> Sender {
        self.sender.clone()
    }

    #[inline(always)]
    pub fn receiver(&self) -> Receiver {
        self.receiver.clone()
    }

    pub async fn _recv(receiver: Receiver) -> PyResult<Option<Message>> {
        let mut lock = receiver.lock().await;
        lock.as_mut()
            .ok_or_else(|| Error::WebSocketDisconnect)?
            .try_next()
            .await
            .map(|val| val.map(Message))
            .map_err(Error::RquestError)
            .map_err(Into::into)
    }

    pub async fn _send(sender: Sender, message: Message) -> PyResult<()> {
        let mut lock = sender.lock().await;
        lock.as_mut()
            .ok_or_else(|| Error::WebSocketDisconnect)?
            .send(message.0)
            .await
            .map_err(Error::RquestError)
            .map_err(Into::into)
    }

    pub async fn _close(
        receiver: Receiver,
        sender: Sender,
        code: Option<u16>,
        reason: Option<PyBackedStr>,
    ) -> PyResult<()> {
        let mut lock = receiver.lock().await;
        let receiver = lock.take();
        drop(lock);
        drop(receiver);

        let mut lock = sender.lock().await;
        let sender = lock.take();
        drop(lock);

        if let Some(mut sender) = sender {
            let reason = reason
                .map(Bytes::from_owner)
                .map(Utf8Bytes::from_bytes_unchecked)
                .unwrap_or_else(|| rquest::Utf8Bytes::from_static("Goodbye"));
            sender
                .send(rquest::Message::Close(Some(rquest::CloseFrame {
                    code: code
                        .map(rquest::CloseCode)
                        .unwrap_or(rquest::CloseCode::NORMAL),

                    reason,
                })))
                .await
                .map_err(Error::RquestError)?;
            sender.flush().await.map_err(Error::RquestError)?;
            sender.close().await.map_err(Error::RquestError)?;
        }

        Ok(())
    }

    pub async fn _anext(
        receiver: Receiver,
        py_stop_iteration_error: fn() -> PyErr,
    ) -> PyResult<Message> {
        let mut lock = receiver.lock().await;
        let val = lock
            .as_mut()
            .ok_or_else(py_stop_iteration_error)?
            .try_next()
            .await;

        drop(lock);

        val.map(|val| val.map(Message))
            .map_err(Error::RquestError)?
            .ok_or_else(py_stop_iteration_error)
    }
}

#[cfg_attr(feature = "docs", gen_stub_pymethods)]
#[pymethods]
impl WebSocket {
    /// Returns whether the response is successful.
    #[getter]
    #[inline(always)]
    pub fn ok(&self) -> bool {
        self.status_code.as_int() == rquest::StatusCode::SWITCHING_PROTOCOLS
    }

    /// Returns the status code as integer of the response.
    #[getter]
    #[inline(always)]
    pub fn status(&self) -> u16 {
        self.status_code.as_int()
    }

    /// Returns the status code of the response.
    #[getter]
    #[inline(always)]
    pub fn status_code(&self) -> StatusCode {
        self.status_code
    }

    /// Returns the HTTP version of the response.
    #[getter]
    #[inline(always)]
    pub fn version(&self) -> Version {
        self.version
    }

    /// Returns the headers of the response.
    #[getter]
    #[inline(always)]
    pub fn headers(&self) -> HeaderMap {
        HeaderMap(self.headers.clone())
    }

    /// Returns the cookies of the response.
    #[getter]
    #[inline(always)]
    pub fn cookies<'py>(&'py self, py: Python<'py>) -> Vec<Cookie> {
        py.allow_threads(|| Cookie::extract_cookies(&self.headers))
    }

    /// Returns the remote address of the response.
    #[getter]
    #[inline(always)]
    pub fn remote_addr(&self) -> Option<SocketAddr> {
        self.remote_addr
    }

    /// Returns the WebSocket protocol.
    #[inline(always)]
    pub fn protocol(&self) -> Option<&str> {
        self.protocol
            .as_ref()
            .map(HeaderValue::to_str)
            .transpose()
            .ok()
            .flatten()
    }

    /// Receives a message from the WebSocket.
    #[inline(always)]
    pub fn recv<'rt>(&self, py: Python<'rt>) -> PyResult<Bound<'rt, PyAny>> {
        future_into_py(py, Self::_recv(self.receiver.clone()))
    }

    /// Sends a message to the WebSocket.
    ///
    /// # Arguments
    ///
    /// * `message` - The message to send.
    #[pyo3(signature = (message))]
    #[inline(always)]
    pub fn send<'rt>(&self, py: Python<'rt>, message: Message) -> PyResult<Bound<'rt, PyAny>> {
        future_into_py(py, Self::_send(self.sender.clone(), message))
    }

    /// Closes the WebSocket connection.
    ///
    /// # Arguments
    ///
    /// * `code` - An optional close code.
    /// * `reason` - An optional reason for closing.
    #[pyo3(signature = (code=None, reason=None))]
    #[inline(always)]
    pub fn close<'rt>(
        &self,
        py: Python<'rt>,
        code: Option<u16>,
        reason: Option<PyBackedStr>,
    ) -> PyResult<Bound<'rt, PyAny>> {
        let sender = self.sender.clone();
        let receiver = self.receiver.clone();
        future_into_py(py, Self::_close(receiver, sender, code, reason))
    }
}

#[cfg_attr(feature = "docs", gen_stub_pymethods)]
#[pymethods]
impl WebSocket {
    #[inline(always)]
    fn __aiter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    #[inline(always)]
    fn __anext__<'rt>(&self, py: Python<'rt>) -> PyResult<Bound<'rt, PyAny>> {
        future_into_py(
            py,
            WebSocket::_anext(self.receiver.clone(), || Error::StopAsyncIteration.into()),
        )
    }

    #[inline(always)]
    fn __aenter__<'a>(slf: PyRef<'a, Self>, py: Python<'a>) -> PyResult<Bound<'a, PyAny>> {
        let slf = slf.into_py_any(py)?;
        future_into_py(py, async move { Ok(slf) })
    }

    #[inline(always)]
    fn __aexit__<'a>(
        &self,
        py: Python<'a>,
        _exc_type: &Bound<'a, PyAny>,
        _exc_value: &Bound<'a, PyAny>,
        _traceback: &Bound<'a, PyAny>,
    ) -> PyResult<Bound<'a, PyAny>> {
        self.close(py, None, None)
    }
}
