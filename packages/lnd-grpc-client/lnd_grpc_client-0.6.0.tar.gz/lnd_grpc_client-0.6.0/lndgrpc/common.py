import binascii
import platform
import os
import grpc
import sys
from pathlib import Path

from lndgrpc.compiled import (
    lightning_pb2 as ln,
    lightning_pb2_grpc as lnrpc,
    router_pb2 as router,
    router_pb2_grpc as routerrpc,
    verrpc_pb2 as ver,
    verrpc_pb2_grpc as verrpc,
    walletkit_pb2 as walletkit,
    walletkit_pb2_grpc as walletkitrpc,
    signer_pb2 as signer,
    signer_pb2_grpc as signerrpc,
    walletunlocker_pb2 as walletunlocker,
    walletunlocker_pb2_grpc as walletunlockerrpc,
    invoices_pb2 as invoices,
    invoices_pb2_grpc as invoicesrpc,
    stateservice_pb2 as stateservice,
    stateservice_pb2_grpc as stateservicerpc,
    dev_pb2 as dev,
    dev_pb2_grpc as devrpc,
    autopilot_pb2 as autopilot,
    autopilot_pb2_grpc as autopilotrpc,
    neutrino_pb2 as neutrino,
    neutrino_pb2_grpc as neutrinorpc,
    peers_pb2 as peers,
    peers_pb2_grpc as peersrpc,
    watchtower_pb2 as watchtower,
    watchtower_pb2_grpc as watchtowerrpc,
    wtclient_pb2 as wtclient,
    wtclient_pb2_grpc as wtclientrpc,
    chainnotifier_pb2 as chainnotifier,
    chainnotifier_pb2_grpc as chainnotifierrpc,
)

system = platform.system().lower()

if system == 'linux':
    TLS_FILEPATH = os.path.expanduser('~/.lnd/tls.cert')
    ADMIN_MACAROON_BASE_FILEPATH = '~/.lnd/data/chain/bitcoin/{}/admin.macaroon'
    READ_ONLY_MACAROON_BASE_FILEPATH = '~/.lnd/data/chain/bitcoin/{}/readonly.macaroon'
elif system == 'darwin':
    TLS_FILEPATH = os.path.expanduser('~/Library/Application Support/Lnd/tls.cert')
    ADMIN_MACAROON_BASE_FILEPATH = '~/Library/Application Support/Lnd/data/chain/bitcoin/{}/admin.macaroon'
    READ_ONLY_MACAROON_BASE_FILEPATH = '~/Library/Application Support/Lnd/data/chain/bitcoin/{}/readonly.macaroon'
elif system == 'windows':
    TLS_FILEPATH = os.path.join(os.path.expanduser("~"), 'AppData', 'Local', 'Lnd', 'tls.cert')
    ADMIN_MACAROON_BASE_FILEPATH = os.path.join(os.path.expanduser("~"), 'AppData', 'Local', 'Lnd', 'data', 'chain', 'bitcoin', 'mainnet', 'admin.macaroon')
    READ_ONLY_MACAROON_BASE_FILEPATH = os.path.join(os.path.expanduser("~"), 'AppData', 'Local', 'Lnd', 'data', 'chain', 'bitcoin', 'mainnet', 'readonly.macaroon')
else:
    raise SystemError('Unrecognized system')


# Due to updated ECDSA generated tls.cert we need to let gprc know that
# we need to use that cipher suite otherwise there will be a handhsake
# error when we communicate with the lnd rpc server.
os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'


def get_cert(filepath=None):
    """Read in tls.cert from file

    Note: tls files need to be read in byte mode as of grpc 1.8.2
          https://github.com/grpc/grpc/issues/13866
    """
    filepath = filepath or TLS_FILEPATH
    with open(filepath, 'rb') as f:
        cert = f.read()
    return cert


def get_macaroon(filepath=None):
    """Read and decode macaroon from file

    The macaroon is decoded into a hex string and returned.
    """
    if filepath is None:
        print("Must specify macaroon_filepath")
        sys.exit(1)

    with open(filepath, 'rb') as f:
        macaroon_bytes = f.read()
    return binascii.hexlify(macaroon_bytes).decode()


def generate_credentials(cert, macaroon):
    """Create composite channel credentials using cert and macaroon metadata"""
    # create cert credentials from the tls.cert file
    # if os.getenv("LND_HTTPS_TLS"):
    #     cert_creds = grpc.ssl_channel_credentials()
    # else:
    cert_creds = grpc.ssl_channel_credentials(cert)

    # build meta data credentials
    metadata_plugin = MacaroonMetadataPlugin(macaroon)
    auth_creds = grpc.metadata_call_credentials(metadata_plugin)

    # combine the cert credentials and the macaroon auth credentials
    # such that every call is properly encrypted and authenticated
    return grpc.composite_channel_credentials(cert_creds, auth_creds)


class MacaroonMetadataPlugin(grpc.AuthMetadataPlugin):
    """Metadata plugin to include macaroon in metadata of each RPC request"""

    def __init__(self, macaroon):
        self.macaroon = macaroon

    def __call__(self, context, callback):
        callback([('macaroon', self.macaroon)], None)


class BaseClient(object):
    grpc_module = grpc

    def __init__(
        self,
        ip_address=None,
        cert=None,
        cert_filepath=None,
        no_tls=False,
        macaroon=None,
        macaroon_filepath=None
    ):

# # CASE 1: A folder with tls.cert, and admin.macaroon
# export LND_CRED_PATH=/home/user/creds/my_favorite_node/lnd

# # CASE 2: Running directly on a machine running LND
# export LND_ROOT_DIR=/home/user/.lnd
# export LND_NETWORK=mainnet

        credential_path = os.getenv("LND_CRED_PATH", None)
        root_dir = os.getenv("LND_ROOT_DIR", None)
        network = os.getenv("LND_NETWORK", None)
        node_ip = os.getenv("LND_NODE_IP")
        node_port = os.getenv("LND_NODE_PORT")
        lnd_macaroon = os.getenv("LND_MACAROON", "admin.macaroon")
        # Handle either passing in credentials_paths, or environment variable paths

        # IF credential_path
        # ELIF root_dir + network
        # ELSE use passed in macaroon_filepath and cert_filepath
        # ELSE use macaroon, and cert

        if credential_path:
            credential_path = Path(credential_path)
            macaroon_filepath = str(credential_path.joinpath(lnd_macaroon).absolute())
            cert_filepath = str(credential_path.joinpath("tls.cert").absolute())

        elif root_dir and network:
            macaroon_filepath = str(root_dir.joinpath(f"data/chain/bitcoin/{network}/admin.macaroon").absolute())
            cert_filepath = str(root_dir.joinpath("tls.cert").absolute())

        elif (macaroon_filepath and cert_filepath) or (macaroon and cert):
            pass
        
        else:
            print("Missing credentials!")
            sys.exit(1)



        # if macaroon_filepath is None and macaroon is None:
        #     if credential_path != None:


        #     elif root_dir != None and != network != None:
        #         if credential_path != None:
        #         credential_path = Path(root_dir)
        #         macaroon_filepath = str(credential_path.joinpath(f"data/chain/bitcoin/{network}/admin.macaroon").absolute())

        #     else:
        #         print("Must specify LND_CRED_PATH, or LND_ROOT_DIR + LND_NETWORK environment variables!")
        #         sys.exit(1)


        # if cert_filepath is None and cert is None:
        #     credential_path = os.getenv("LND_CRED_PATH", None)
        #     credential_path = Path(credential_path)
        #     cert_filepath = str(credential_path.joinpath("tls.cert").absolute())

        #     if credential_path != None:
        #         credential_path = Path(credential_path)
        #         cert_filepath = str(credential_path.joinpath("tls.cert").absolute())

        #     elif root_dir != None and != network != None:
        #         if credential_path != None:
        #         credential_path = Path(root_dir)
        #         macaroon_filepath = str(credential_path.joinpath(f"data/chain/bitcoin/{network}/admin.macaroon").absolute())

        #     else:
        #         print("Must specify LND_CRED_PATH, or LND_ROOT_DIR + LND_NETWORK environment variables!")
        #         sys.exit(1)


        if ip_address is None:
            ip_address = f"{node_ip}:{node_port}"

        # handle passing in credentials and cert directly
        if macaroon is None:
            macaroon = get_macaroon(filepath=macaroon_filepath)

        if cert is None and no_tls == False:
            cert = get_cert(cert_filepath)

        self._credentials = generate_credentials(cert, macaroon)
        self.ip_address = ip_address

    @property
    def _ln_stub(self):
        """Create a ln_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address,
            self._credentials, 
            # timeout=30,
            options=[('grpc.max_receive_message_length', 1024*1024*50), ("grpc.max_connection_idle_ms", 30000)]
        )
        return lnrpc.LightningStub(channel)

    @property
    def _router_stub(self):
        """Create a ln_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return routerrpc.RouterStub(channel)

    @property
    def _walletunlocker_stub(self):
        """Create a wallet_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return walletunlockerrpc.WalletUnlockerStub(channel)

    @property
    def _wallet_stub(self):
        """Create a wallet_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return lnrpc.WalletUnlockerStub(channel)

    @property
    def _walletkit_stub(self):
        """Create a wallet_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return walletkitrpc.WalletKitStub(channel)

    @property
    def _signer_stub(self):
        """Create a wallet_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return signerrpc.SignerStub(channel)


    @property
    def _version_stub(self):
        """Create a version_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return verrpc.VersionerStub(channel)

    @property
    def _invoices_stub(self):
        """Create a version_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return invoicesrpc.InvoicesStub(channel)

    @property
    def _invoices_servicer_stub(self):
        """Create a version_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return invoicesrpc.InvoicesServicer(channel)

    @property
    def _state_stub(self):
        """Create a version_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return stateservicerpc.StateStub(channel)

    @property
    def _dev_stub(self):
        """Create a version_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return devrpc.DevStub(channel)

    @property
    def _neutrino_stub(self):
        """Create a version_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return neutrinorpc.NeutrinoKitStub(channel)

    @property
    def _peer_stub(self):
        """Create a version_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return peerrpc.PeersStub(channel)
    
    @property
    def _watchtower_stub(self):
        """Create a version_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return watchtowerrpc.WatchtowerStub(channel)

    @property
    def _wtclient_stub(self):
        """Create a version_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return wtclientrpc.WatchtowerClientStub(channel)


    @property
    def _autopilot_stub(self):
        """Create a version_stub dynamically to ensure channel freshness

        If we make a call to the Lightning RPC service when the wallet
        is locked or the server is down we will get back an RPCError with
        StatusCode.UNAVAILABLE which will make the channel unusable.
        To ensure the channel is usable we create a new one for each request.
        """
        channel = self.grpc_module.secure_channel(
            self.ip_address, self._credentials, options=[('grpc.max_receive_message_length', 1024*1024*50)]
        )
        return autopilotrpc.AutopilotStub(channel)