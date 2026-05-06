from .IMessage import IMessage

class MessageImpl(IMessage):
    """ Message envoyé vers la passerelle"""

    message_id: int
    source: str
    destination: str
    timestamp: float

    def __init__(self, message_id, source, destination, timestamp=0.0):
        self._message_id = message_id
        self._source = source
        self._destination = destination
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

    def set_destination(self, destination):
        self._destination = destination

    ### setters du message ###
    def set_timestamp(self, temps):
        self._timestamp = temps

    # --- Affichage ---
    def print_message(self):
        return(f"[Message] ID={self._message_id} | src={self._source} "
              f"| dst={self._destination} | timestamp={self._timestamp:.4f}")
