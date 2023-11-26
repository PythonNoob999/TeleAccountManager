from .send_message import SendMessage
from .join_chats import JoinChats
from .leave_chats import LeaveChats
from .ref import Ref
from .click import Click
from .send_contact import SendContact
from .add_contact import AddContact
from .send_reaction import SendReaction
from .send_vote import SendVote
from .unsend_vote import UnsendVote

class Methods(
SendMessage,
JoinChats,
LeaveChats,
Ref,
Click,
SendContact,
AddContact,
SendReaction,
SendVote,
UnsendVote
):
    pass
