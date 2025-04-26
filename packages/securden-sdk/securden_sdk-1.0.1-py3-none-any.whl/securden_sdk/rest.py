# coding: utf-8

import io
import json
import re
import ssl
import socket
import tempfile
import warnings

import urllib3

from securden_sdk.exceptions import ApiException, ApiValueError

SUPPORTED_SOCKS_PROXIES = {"socks5", "socks5h", "socks4", "socks4a"}
RESTResponseType = urllib3.HTTPResponse

def is_socks_proxy_url(url):
    if url is None:
        return False
    split_section = url.split("://")
    if len(split_section) < 2:
        return False
    else:
        return split_section[0].lower() in SUPPORTED_SOCKS_PROXIES

class RESTResponse(io.IOBase):

    def __init__(self, resp) -> None:
        self.response = resp
        self.status = resp.status
        self.reason = resp.reason
        self.data = None

    def read(self):
        if self.data is None:
            self.data = self.response.data
        return self.data

    def getheaders(self):
        """Returns a dictionary of the response headers."""
        return self.response.headers

    def getheader(self, name, default=None):
        """Returns a given response header."""
        return self.response.headers.get(name, default)

class RESTClientObject:

    def __init__(self, configuration) -> None:
        # urllib3.PoolManager will pass all kw parameters to connectionpool
        # Custom SSL certificates and client certificates: http://urllib3.readthedocs.io/en/latest/advanced-usage.html

        # cert_reqs
        if configuration.verify_ssl:
            cert_reqs = ssl.CERT_REQUIRED
        else:
            cert_reqs = ssl.CERT_NONE

        # If verify_ssl is True and no ssl_ca_cert is provided, fetch the cert
        # try:
        #     if configuration.verify_ssl and not configuration.ssl_ca_cert:
        #         host, port = self._extract_host_port(configuration.host)
        #         server_cert = ssl.get_server_certificate((host, port))
        #         print("cert ", server_cert)
        #         temp_cert_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
        #         temp_cert_file.write(server_cert.encode("utf-8"))
        #         temp_cert_file.close()
        #         configuration.ssl_ca_cert = temp_cert_file.name
        # except Exception as e:
        #     pass
        
            
        if configuration.verify_ssl:
            host, port = self._extract_host_port(configuration.host)
            is_signed = self._is_signed_cert_type(host, port)

            if is_signed and configuration.ssl_ca_cert:
                warnings.warn(
                    "For signed certificates, ssl_ca_cert is not required. "
                    "The certificate will be fetched from the server. "
                    "Hence, ssl_ca_cert is set to None."
                )
                configuration.ssl_ca_cert = None

            elif not configuration.ssl_ca_cert and not is_signed:
                try:
                    server_cert = ssl.get_server_certificate((host, port))
                except Exception as e:
                    raise RuntimeError(f"Failed to fetch server certificate: {e}")

                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pem") as temp_cert_file:
                        temp_cert_file.write(server_cert.encode("utf-8"))
                        configuration.ssl_ca_cert = temp_cert_file.name
                except Exception as e:
                    raise RuntimeError(f"Failed to create temporary certificate file: {e}")



        pool_args = {
            "cert_reqs": cert_reqs,
            "ca_certs": configuration.ssl_ca_cert,
            "cert_file": configuration.cert_file,
            "key_file": configuration.key_file,
        }
        if configuration.assert_hostname is not None:
            pool_args['assert_hostname'] = (
                configuration.assert_hostname
            )

        if configuration.retries is not None:
            pool_args['retries'] = configuration.retries

        if configuration.tls_server_name:
            pool_args['server_hostname'] = configuration.tls_server_name

        if configuration.socket_options is not None:
            pool_args['socket_options'] = configuration.socket_options

        if configuration.connection_pool_maxsize is not None:
            pool_args['maxsize'] = configuration.connection_pool_maxsize

        # https pool manager
        self.pool_manager: urllib3.PoolManager
        try:
            if configuration.proxy:
                if is_socks_proxy_url(configuration.proxy):
                    from urllib3.contrib.socks import SOCKSProxyManager
                    pool_args["proxy_url"] = configuration.proxy
                    pool_args["headers"] = configuration.proxy_headers
                    self.pool_manager = SOCKSProxyManager(**pool_args)
                else:
                    pool_args["proxy_url"] = configuration.proxy
                    pool_args["proxy_headers"] = configuration.proxy_headers
                    self.pool_manager = urllib3.ProxyManager(**pool_args)
            else:
                self.pool_manager = urllib3.PoolManager(**pool_args)
        except Exception as e:
            print("e    ", e)

    def _extract_host_port(self, host_url):
        """Extracts the host and port from the given host URL."""
        match = re.match(r"https?://([^:/]+)(?::(\d+))?", host_url)
        if not match:
            raise ApiValueError(f"Invalid host URL: {host_url}")
        host = match.group(1)
        port = int(match.group(2)) if match.group(2) else 443
        return host, port
    
    def _is_signed_cert_type(self, host, port):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((host, port)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in cert['issuer'])
                    subject = dict(x[0] for x in cert['subject'])
                    if issuer == subject:
                        return False
                    else:
                        return True
        except Exception as e:
            return False

    def request(
        self,
        method,
        url,
        headers=None,
        body=None,
        post_params=None,
        _request_timeout=None
    ):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        """
        method = method.upper()
        assert method in [
            'GET',
            'HEAD',
            'DELETE',
            'POST',
            'PUT',
            'PATCH',
            'OPTIONS'
        ]

        if post_params and body:
            raise ApiValueError(
                "body parameter cannot be used with post_params parameter."
            )

        post_params = post_params or {}
        headers = headers or {}

        timeout = None
        if _request_timeout:
            if isinstance(_request_timeout, (int, float)):
                timeout = urllib3.Timeout(total=_request_timeout)
            elif (
                    isinstance(_request_timeout, tuple)
                    and len(_request_timeout) == 2
                ):
                timeout = urllib3.Timeout(
                    connect=_request_timeout[0],
                    read=_request_timeout[1]
                )

        try:
            # For `POST`, `PUT`, `PATCH`, `OPTIONS`, `DELETE`
            if method in ['POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE']:

                # no content type provided or payload is json
                content_type = headers.get('Content-Type')
                if (
                    not content_type
                    or re.search('json', content_type, re.IGNORECASE)
                ):
                    request_body = None
                    if body is not None:
                        request_body = json.dumps(body)
                    r = self.pool_manager.request(
                        method,
                        url,
                        body=request_body,
                        timeout=timeout,
                        headers=headers,
                        preload_content=False
                    )
                elif content_type == 'application/x-www-form-urlencoded':
                    r = self.pool_manager.request(
                        method,
                        url,
                        fields=post_params,
                        encode_multipart=False,
                        timeout=timeout,
                        headers=headers,
                        preload_content=False
                    )
                elif content_type == 'multipart/form-data':
                    del headers['Content-Type']
                    post_params = [(a, json.dumps(b)) if isinstance(b, dict) else (a,b) for a, b in post_params]
                    r = self.pool_manager.request(
                        method,
                        url,
                        fields=post_params,
                        encode_multipart=True,
                        timeout=timeout,
                        headers=headers,
                        preload_content=False
                    )
                elif isinstance(body, str) or isinstance(body, bytes):
                    r = self.pool_manager.request(
                        method,
                        url,
                        body=body,
                        timeout=timeout,
                        headers=headers,
                        preload_content=False
                    )
                elif headers['Content-Type'].startswith('text/') and isinstance(body, bool):
                    request_body = "true" if body else "false"
                    r = self.pool_manager.request(
                        method,
                        url,
                        body=request_body,
                        preload_content=False,
                        timeout=timeout,
                        headers=headers)
                else:
                    msg = """Cannot prepare a request message for provided
                             arguments. Please check that your arguments match
                             declared content type."""
                    raise ApiException(status=0, reason=msg)
            else:
                r = self.pool_manager.request(
                    method,
                    url,
                    fields={},
                    timeout=timeout,
                    headers=headers,
                    preload_content=False
                )
        except urllib3.exceptions.SSLError as e:
            msg = "\n".join([type(e).__name__, str(e)])
            raise ApiException(status=0, reason=msg)

        return RESTResponse(r)
