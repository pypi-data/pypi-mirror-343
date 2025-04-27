use crate::{
    async_impl::{self, Message},
    error::Error,
    typing::{Cookie, HeaderMap, SocketAddr, StatusCode, Version},
};
use pyo3::{prelude::*, pybacked::PyBackedStr};
#[cfg(feature = "docs")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};
use std::ops::Deref;

/// A blocking WebSocket response.
#[cfg_attr(feature = "docs", gen_stub_pyclass)]
#[pyclass]
pub struct BlockingWebSocket(async_impl::WebSocket);

impl From<async_impl::WebSocket> for BlockingWebSocket {
    fn from(inner: async_impl::WebSocket) -> Self {
        Self(inner)
    }
}

impl Deref for BlockingWebSocket {
    type Target = async_impl::WebSocket;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[cfg_attr(feature = "docs", gen_stub_pymethods)]
#[pymethods]
impl BlockingWebSocket {
    /// Returns whether the response is successful.
    #[getter]
    #[inline(always)]
    pub fn ok(&self) -> bool {
        self.0.ok()
    }

    /// Returns the status code as integer of the response.
    #[getter]
    #[inline(always)]
    pub fn status(&self) -> u16 {
        self.0.status()
    }

    /// Returns the status code of the response.
    #[getter]
    #[inline(always)]
    pub fn status_code(&self) -> StatusCode {
        self.0.status_code()
    }

    /// Returns the HTTP version of the response.
    #[getter]
    #[inline(always)]
    pub fn version(&self) -> Version {
        self.0.version()
    }

    /// Returns the headers of the response.
    #[getter]
    #[inline(always)]
    pub fn headers(&self) -> HeaderMap {
        self.0.headers()
    }

    /// Returns the cookies of the response.
    #[getter]
    #[inline(always)]
    pub fn cookies<'py>(&'py self, py: Python<'py>) -> Vec<Cookie> {
        self.0.cookies(py)
    }

    /// Returns the remote address of the response.
    #[getter]
    #[inline(always)]
    pub fn remote_addr(&self) -> Option<SocketAddr> {
        self.0.remote_addr()
    }

    /// Returns the WebSocket protocol.
    #[inline(always)]
    pub fn protocol(&self) -> Option<&str> {
        self.0.protocol()
    }

    /// Receives a message from the WebSocket.
    #[inline(always)]
    pub fn recv(&self, py: Python) -> PyResult<Option<Message>> {
        py.allow_threads(|| {
            pyo3_async_runtimes::tokio::get_runtime()
                .block_on(async_impl::WebSocket::_recv(self.receiver()))
        })
    }

    /// Sends a message to the WebSocket.
    ///
    /// # Arguments
    ///
    /// * `message` - The message to send.
    #[pyo3(signature = (message))]
    #[inline(always)]
    pub fn send(&self, py: Python, message: Message) -> PyResult<()> {
        py.allow_threads(|| {
            pyo3_async_runtimes::tokio::get_runtime()
                .block_on(async_impl::WebSocket::_send(self.sender(), message))
        })
    }

    /// Closes the WebSocket connection.
    ///
    /// # Arguments
    ///
    /// * `code` - An optional close code.
    /// * `reason` - An optional reason for closing.
    #[pyo3(signature = (code=None, reason=None))]
    #[inline(always)]
    pub fn close(
        &self,
        py: Python,
        code: Option<u16>,
        reason: Option<PyBackedStr>,
    ) -> PyResult<()> {
        py.allow_threads(|| {
            pyo3_async_runtimes::tokio::get_runtime().block_on(async_impl::WebSocket::_close(
                self.receiver(),
                self.sender(),
                code,
                reason,
            ))
        })
    }
}

#[cfg_attr(feature = "docs", gen_stub_pymethods)]
#[pymethods]
impl BlockingWebSocket {
    #[inline(always)]
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    #[inline(always)]
    fn __next__(&self, py: Python) -> PyResult<Message> {
        py.allow_threads(|| {
            pyo3_async_runtimes::tokio::get_runtime()
                .block_on(async_impl::WebSocket::_anext(self.receiver(), || {
                    Error::StopIteration.into()
                }))
        })
    }

    #[inline(always)]
    fn __enter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    #[inline(always)]
    fn __exit__<'a>(
        &self,
        py: Python<'a>,
        _exc_type: &Bound<'a, PyAny>,
        _exc_value: &Bound<'a, PyAny>,
        _traceback: &Bound<'a, PyAny>,
    ) -> PyResult<()> {
        self.close(py, None, None)
    }
}
