# Copyright (C) 2007-2010 Samuel Abels.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
Representing a device to connect with.
"""
from util.cast import to_list
from util.ipv4 import is_ip
from util.url  import parse_url, Url

def _is_ip(string):
    # Adds IPv6 support.
    return ':' in string or is_ip(string)

class Host(object):
    """
    Represents a device on which to open a connection.
    """

    def __init__(self, uri, default_protocol = 'telnet'):
        """
        Constructor. The given uri is passed to Host.set_uri().
        The default_protocol argument defines the protocol that is used
        in case the given uri does not specify it.

        @type  uri: string
        @param uri: A hostname; see set_uri() for more info.
        @type  default_protocol: string
        @param default_protocol: The protocol name.
        """
        self.protocol  = default_protocol
        self.vars      = {}
        self.username  = None
        self.password1 = None
        self.password2 = None
        self.logname   = None
        self.set_uri(uri) 


    def set_uri(self, uri):
        """
        Defines the protocol, hostname/address, TCP port number, username,
        and password from the given URL. The hostname may be URL formatted,
        so the following formats are all valid:

            - myhostname
            - myhostname.domain
            - ssh:hostname
            - ssh:hostname.domain
            - ssh://hostname
            - ssh://user@hostname
            - ssh://user:password@hostname
            - ssh://user:password@hostname:21

        For a list of supported protocols please see set_protocol().

        @type  uri: string
        @param uri: An URL formatted hostname.
        """
        try:
            uri = parse_url(uri, self.protocol)
        except ValueError, e:
            raise ValueError('Hostname parse error: ' + repr(uri))
        hostname = uri.hostname or ''
        name     = uri.path and hostname + uri.path or hostname
        self.set_protocol(uri.protocol)
        self.set_tcp_port(uri.port)
        self.set_name(name)
        self.set_address(name)
        self.set_username(uri.username)
        self.set_password(uri.password1)
        self.set_password2(uri.password2)

        for key, val in uri.vars.iteritems():
            self.set(key, val)


    def get_uri(self):
        url = Url()
        url.protocol  = self.get_protocol()
        url.username  = self.get_username()
        url.password1 = self.get_password()
        url.password2 = self.get_password2()
        url.hostname  = self.get_address()
        url.port      = self.get_tcp_port()
        url.vars      = dict((k, to_list(v))
                             for (k, v) in self.get_all().iteritems())
        return str(url)

    def set_name(self, name):
        """
        Set the hostname of the remote host without
        changing username, password, protocol, and TCP port number.

        @type  name: string
        @param name: A hostname or IP address.
        """
        self.name = name


    def get_name(self):
        """
        Returns the name.

        @rtype:  string
        @return: The hostname excluding the name.
        """
        return self.name


    def set_address(self, address):
        """
        Set the address of the remote host the is contacted, without
        changing hostname, username, password, protocol, and TCP port
        number.
        This is the actual address that is used to open the connection.

        @type  address: string
        @param address: A hostname or IP name.
        """
        self.address = address


    def get_address(self):
        """
        Returns the address that is used to open the connection.

        @rtype:  string
        @return: The address that is used to open the connection.
        """
        return self.address


    def set_protocol(self, protocol):
        """
        Defines the protocol. The following protocols are currently
        supported:

            - telnet: Telnet
            - ssh1: SSH version 1
            - ssh2: SSH version 2
            - ssh: Automatically selects the best supported SSH version
            - dummy: A virtual device that accepts any command, but that
              does not respond anything useful.
            - pseudo: A virtual device that loads a file with the given
              "hostname". The given file is a Python file containing
              information on how the virtual device shall respond to
              commands. For more information please refer to the
              documentation of
              protocols.Dummy.load_command_handler_from_file().

        @type  protocol: string
        @param protocol: The protocol name.
        """
        self.protocol = protocol


    def get_protocol(self):
        """
        Returns the name of the protocol.

        @rtype:  string
        @return: The protocol name.
        """
        return self.protocol


    def set_tcp_port(self, tcp_port):
        """
        Defines the TCP port number.

        @type  tcp_port: int
        @param tcp_port: The TCP port number.
        """
        self.tcp_port = tcp_port


    def get_tcp_port(self):
        """
        Returns the TCP port number.

        @rtype:  string
        @return: The TCP port number.
        """
        return self.tcp_port


    def set_username(self, name):
        """
        Defines the username of the account that is used to log in.

        @type  name: string
        @param name: The username.
        """
        self.username = name


    def get_username(self):
        """
        Returns the username of the account that is used to log in.

        @rtype:  string
        @return: The username.
        """
        return self.username


    def set_password(self, password):
        """
        Defines the password of the account that is used to log in.

        @type  password: string
        @param password: The password.
        """
        self.password1 = password


    def get_password(self):
        """
        Returns the password of the account that is used to log in.

        @rtype:  string
        @return: The password.
        """
        return self.password1


    def set_password2(self, password):
        """
        Defines an alternate password. This is used, for example in any
        place where auto_authorize() is called.

        @type  password: string
        @param password: The password.
        """
        self.password2 = password


    def get_password2(self):
        """
        Returns the password of the account that is used to log in.

        @rtype:  string
        @return: The password.
        """
        return self.password2


    def set_logname(self, logname):
        """
        Defines the basename of the log name. The name may include a slash,
        in which case the logs for this host are placed in a subdirectory
        (when a FileLogger is used).
        By default, the logname is the name of the host.

        @type:  string
        @param: The basename of the logfile.
        """
        self.logname = logname


    def get_logname(self):
        """
        Returns the basename of the logfile.

        @rtype:  string
        @return: The basename of the logfile.
        """
        if self.logname:
            return self.logname
        return self.get_name()


    def set(self, name, value):
        """
        Stores the given variable/value in the object for later retrieval.

        @type  name: string
        @param name: The name of the variable.
        @type  value: object
        @param value: The value of the variable.
        """
        self.vars[name] = value


    def set_all(self, vars):
        """
        Like set(), but replaces all variables by using the given
        dictionary. In other words, passing an empty dictionary
        results in all variables being removed.

        @type  vars: dict
        @param vars: The dictionary with the variables.
        """
        self.vars = dict(vars)


    def append(self, name, value):
        """
        Appends the given value to the list variable with the given name.

        @type  name: string
        @param name: The name of the variable.
        @type  value: object
        @param value: The appended value.
        """
        if self.vars.has_key(name):
            self.vars[name].append(value)
        else:
            self.vars[name] = [value]


    def set_default(self, name, value):
        """
        Like set(), but only sets the value if the variable is not already
        defined.

        @type  name: string
        @param name: The name of the variable.
        @type  value: object
        @param value: The value of the variable.
        """
        if not self.vars.has_key(name):
            self.vars[name] = value


    def has_key(self, name):
        """
        Returns True if the variable with the given name is defined, False
        otherwise.

        @type  name: string
        @param name: The name of the variable.
        @rtype:  bool
        @return: Whether the variable is defined.
        """
        return self.vars.has_key(name)


    def get(self, name, default = None):
        """
        Returns the value of the given variable, or the given default
        value if the variable is not defined.

        @type  name: string
        @param name: The name of the variable.
        @type  default: object
        @param default: The default value.
        @rtype:  object
        @return: The value of the variable.
        """
        return self.vars.get(name, default)


    def get_all(self):
        """
        Returns a dictionary containing all variables.

        @rtype:  dict
        @return: The dictionary with the variables.
        """
        return self.vars
