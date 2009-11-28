import struct
import logging

from twisted.internet.protocol import Protocol, ServerFactory

import util

class GamespyAuth(Protocol):

   def connectionMade(self):
      self.log = util.getLogger('gamespy.auth', self)

   def dataReceived(self, data):
      hdrFmt = '!4s4sL'
      hLen = struct.calcsize(hdrFmt)
      lgr, err, length = struct.unpack(hdrFmt, data[:hLen])
      data = data[hLen:]
      self.log.debug('received: {0}'.format(repr(data)))

      #HACKy handling for quick and dirty impl.
      if data.startswith('STR=00000000'):
         # initial message.
         # no body to the response.
         self.transport.write(struct.pack(hdrFmt, lgr, '\x00'*4, hLen))
      elif data.startswith('STR'):
         self.transport.loseConnection()

class GamespyAuthFactory(ServerFactory):
   protocol = GamespyAuth

