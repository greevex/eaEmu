import md5
import base64

class PasswordChecker(object):
   def __init__(self, password):
      self.password = password

   def check(self, input):
      return False

class PlainTextPassword(PasswordChecker):
   def check(self, input):
      return self.password == input

class PhpPassword(PasswordChecker):
   def __init__(self, input):
      super(type(self), self).__init__(input)
      self.prefix = '$H$'
      self.regAlph64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
      self.phpAlph64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

   def check(self, input):
      '''
      This algorithm is adapted from the Portable PHP Password Hashing Framework by Alexander Chemeris
      http://www.openwall.com/phpass/

      It was written pretty sloppily, so I cleaned it up.
      '''
      if not self.password.startswith(self.prefix) or len(self.password) < 12:
         return False

      count_log2 = self.phpAlph64.index(self.password[3])
      if count_log2<7 or count_log2>30:
         #raise Exception('Bad count_log2')
         return False
      count = 1<<count_log2

      salt = self.password[4:12]
      if len(salt) != 8:
         raise Exception('hash not long enough')

      m = md5.new(salt)
      m.update(input)
      tmp_hash = m.digest()
      for i in xrange(count):
         m = md5.new(tmp_hash)
         m.update(input)
         tmp_hash = m.digest()

      def reverse64(data):
         np = 3 - len(data) % 3 ## number of pad chars
         data = ''.join('\x00' for _ in range(np)) + data[::-1]
         return base64.b64encode(data)[:np-1 if np else None:-1]
      ## PHP base64 takes reads hexlets right to left rather than left to right...
      match = self.password == self.password[:12] + base64._translate(reverse64(tmp_hash), dict(zip(self.regAlph64, self.phpAlph64)))
      return match
