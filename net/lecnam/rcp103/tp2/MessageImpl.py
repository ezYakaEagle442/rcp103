from .IMessage import IMessage
from net.lecnam.rcp103.tp2.IServer import IServer

class MessageImpl(IMessage):
    """ Message envoyé vers la passerelle (gateway id=0) """

    GATEWAY_ID: int = 0

    message_id: int
    source: int      # node id du client (>= 1)
    destination: int # node id de la destination : 0 = gateway
    timestamp: float

    def __init__(self, message_id, source, destination: int = GATEWAY_ID, timestamp=0.0):
        self._message_id = message_id
        self._source = source
        self._destination = destination  # 0 = gateway par défaut
        self._timestamp = timestamp

    ### getters du message ###
    def get_message_id(self):
        return self._message_id

    def get_source(self):
        return self._source

    def get_destination(self):
        return self._destination

    def get_timestamp(self):
        return self._timestamp

    def set_message_id(self, message_id):
        self._message_id = message_id

    def set_source(self, source):
        self._source = source

    def set_destination(self, destination: int):
        self._destination = destination

    ### setters du message ###
    def set_timestamp(self, temps):
        self._timestamp = temps

    # --- Affichage ---
    def print_message(self):
        dst_label = "gateway" if self._destination == 0 else f"server-{self._destination}"
        return(f"[Message] ID={self._message_id} | src={self._source} "
               f"| dst={self._destination} ({dst_label}) | timestamp={self._timestamp:.4f}")
