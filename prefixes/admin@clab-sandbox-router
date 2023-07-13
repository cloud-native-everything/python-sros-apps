#!/usr/bin/env python3

### pol-change.py
#   Copyright 2023 Nokia
#   mau.rojas@nokia.com
###

"""Test of adding elements to prefix list using pythin script: SR OS 22.5.R2
"""

import re
import sys
from pysros.wrappers import Container
from pysros.management import connect
from pysros.pprint import printTree



def get_connection(host=None, username=None, password=None, port=830):
    """Function definition to obtain a Connection object to a specific
    SR OS device and access the model-driven information.
    :parameter host: The hostname or IP address of the SR OS node.
    :type host: str
    :paramater credentials: The username and password to connect
                            to the SR OS node.
    :type credentials: dict
    :parameter port: The TCP port for the connection to the SR OS node.
    :type port: int
    :returns: Connection object for the SR OS node.
    :rtype: :py:class:`pysros.management.Connection`
    """
    try:
        connection_object = connect(
            host=host,
            username=username,
            password=password,
            port=port,
        )
    except RuntimeError as error1:
        print("Failed to connect.  Error:", error1)
        sys.exit(-1)
    return connection_object


def simple_boolean(_inputstring):
    """Simple function to return True after being called, used to augment
    the Argument classes below. it is meant to be used as a replacement
    for action=store_true in regular argparse
    """
    return True


def simple_string(inputstring):
    """Simple function to return string representation of the argument
    after being called, used to augment the Argument classes below

    :parameter inputstring: The argument passed via sys.argv to be converted
                            to string (if needed) and returned by this function
    :type inputstring: str
    :returns: inputstring as str type
    :rtype: :py:class:`str`
    """
    if isinstance(inputstring, str):
        return inputstring
    return repr(inputstring)


def simple_integer(inputstring):
    """Simple function to return the integer representation of the argument
    after being called, used to augment the Argument classes below

    :parameter inputstring: The argument passed via sys.argv to be converted
                            to an int object and returned by this function
    :type inputstring: str
    :returns: inputstring as int type
    :rtype: :py:class:`int`
    """
    return int(inputstring)


class Argument:
    """Class representing a single CLI argument passed via sys.argv

    :parameter name:    resulting key to be used in the args dictionary to
                        find the value passed for this argument.
    :type name: str
    :parameter parsing_function:    function to be run using the discovered
                                    parameters as input, result of which is
                                    assigned to the variable.
    :type parsing_function: Callable
    :parameter help_text:   Help text to be displayed when needed
    :type help_text: str
    :parameter parameter_modifier:  Number of values to retrieve from
                                    sys.argv to consume for this variable.
    :type parameter_modifier: int
    :parameter default_value:   value assigned by default to ensure args
                                dictionary is always populated.
    :type default_value: Any
    """

    def __init__(
        self,
        _name,
        _parsing_function,
        _help_text,
        _parameter_modifier,
        _default_value,
    ):
        self.name = _name
        self.parsing_function = _parsing_function
        self.help_text = _help_text
        self.parameter_modifier = _parameter_modifier
        self.default_value = _default_value
        self.value = _default_value

    def set_value(self, value):
        """Set the value of this Argument to the passed value parameter
        after it is passed through the object's parsing function.

        :parameter value: The argument passed assigned to the object value
        :type value: Any
        """
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
        self.value = self.parsing_function(value)

    def __str__(self):
        return "%*s" % (20, self.help_text)


class ArgumentHelper:
    """Class acting as abstraction layer between sys.argv and a
    collection of Arguments to be returned as a key:value dictionary
    after parsing and processing.

    Intended to be similar to the ArgumentParser class in argparse.
    """

    def __init__(self):
        self.command_help = "watch help/-h"
        self.arg_list_pointer = 0
        self.args = {}

    def add_argument(self, key, arg):
        """Add an argument to the class' internal args dictionary by key
        with value equal to an Argument.

        :parameter key: CLI flag to be used to specifically address the
                        corresponding Argument object
        :type key: str
        :parameter arg: The Argument object being created and made available
        :type arg: :py:class:`Argument`
        """
        self.args[key] = arg

    def send_help(self):
        """Distill a help message similar to what is shown on Linux CLI
        to be shown on the SR OS CLI when an operator enters the command
        without arguments, or with "-h" or "help" as an argument

        :returns:   a printable help message to be displayed on the CLI, using
                    information found in each Argument contained in self.args
        :rtype: str
        """
        help_message = "\nExample: %-*s\nCommand options:\n" % (
            20,
            "watch.py <command to execute/monitor> %s" % (self.help_flags()),
        )
        for flag, arg in self.args.items():
            help_message += " %-*s%s\n" % (10 + len(flag), flag, arg)
        help_message += " %-*s%s" % (
            10 + len("-h"),
            "-h",
            "Display this message.",
        )
        return help_message

    def help_flags(self):
        """Add an argument to the class' internal args dictionary by key
        with value equal to an Argument.

        :returns:   a printable help message to be displayed on the CLI,
                    showing potentially usable flags in shorthand notation,
                    to be included with the result of send_help
        :rtype: str
        """
        flags = "|".join(
            k + (" #" if v.parameter_modifier > 0 else "")
            for k, v in self.args.items()
        )
        return flags

    def handle_argument(self, index, arg_list_skip_path):
        """Handle an argument specified on the CLI by finding the key, using
        the key to find the Argument object, determining how many parameters
        there should be on the CLI and passing those to the Argument's
        set_value call.

        :parameter index:   Current index in the list of CLI arguments being
                            looked at for parsing/processing
        :type key: int
        :parameter arg_list_skip_path: list of CLI arguments
        :type arg: list
        """
        argument_flag = arg_list_skip_path[index]
        self.arg_list_pointer += self.args[argument_flag].parameter_modifier
        self.args[argument_flag].set_value(
            arg_list_skip_path[index + 1: self.arg_list_pointer + 1]
        )
        self.arg_list_pointer += 1

    def parse_argv(self, _arg_list):
        """Add an argument to the class' args dictionary by key with value
        equal to an Argument.

        :parameter _arg_list:   the list of arguments, retrieved from sys.argv
                                by the caller and passed to this function.
        :type arg: list
        :returns:   a dictionary containing the specified Arguments either with
                    default or specific values, or a "helped" flag that
                    terminates the program.
        :rtype: str
        """
        arg_list = _arg_list
        if len(arg_list) == 0:
            return None

        if len(arg_list) == 1 or arg_list[1] == "-h" or arg_list[1] == "help":
            print(self.send_help())
            return {"helped": True}

        result_args = {}
        # Skip the first element, as that is the path (in this case)
        if arg_list[1] == "/":
            # Elements such as
            #     watch /state/system/up-time
            #     watch /nokia-state:state/system/up-time
            # are passed to arg_list with the first '/' in its
            # own entry in the list: undo that.
            #
            # - this also applies to
            # -     /show system information
            # - that appears "/", "show system information"
            # - avoid, lighten the condition on the if-statement above
            arg_list[1] += arg_list[2]
            del arg_list[2]
        arg_list_skip_path = arg_list[1:]

        # ### ###
        # If this command needs a tools/show/state command to start
        # this section is needed. If not provided it can't run.
        # ### ###
        try:
            # parts of show commands that follow a space and start with '-'
            # may cause a problem in execution however no specific examples
            # of this are known
            self.arg_list_pointer = min(
                (
                    index
                    for index, value in enumerate(arg_list_skip_path)
                    if value.startswith("-")
                )
            )
        except ValueError:
            # ValueError: min() arg is an empty sequence
            self.arg_list_pointer = len(arg_list_skip_path)
        result_args["xpath"] = " ".join(
            arg_list_skip_path[: self.arg_list_pointer]
        )
        # ### ###
        # the arguments come after the show command
        # ### ###
        for index, value in enumerate(arg_list_skip_path):
            if self.arg_list_pointer == index:
                try:
                    self.handle_argument(index, arg_list_skip_path)
                except KeyError as error_cli_option:
                    print(
                        '"%s" is not a valid command option. See \n%s'
                        % (error_cli_option, self.send_help())
                    )
                    sys.exit(98)
            else:
                # this parameter or flag was already used - skip
                pass

        intermediary = {v.name: v.value for _, v in self.args.items()}
        intermediary.update(result_args)
        return intermediary


def leaf_diff(path, key, new, r_exclude):
    """Display the path leading up to the new value of the leaf in tree,
    followed by the new value.

    :parameter path:    The json-instance-path leading up
                        to the leaf of which the value is being compared
    :type path: str
    :parameter key: The specific key for the leaf within the parent Container.
                    Empty if the query was a specific Leaf.
    :type key: str
    :parameter new: The new value found in the leaf
    :type new: str
    :parameter r_exclude:   Regex to exclude any leafs whose name matches this
                            regular expression
    :type r_exclude: str
    """
    output = path + (("/" + str(key)) if key else "") + "/" + str(new)
    if r_exclude is not None:
        if not bool(re.match(r_exclude, output)):
            print(output)
    else:
        print(output)


def dict_diff(ref, new, path, r_exclude):
    """Display the path leading up to one of three possible situations;
        either a leaf is removed from the tree or
        a leaf is added to the tree or
        a leaf's value has changed

    :parameter ref: The reference value, for the currently new values to be
                    compared against
    :type ref: str
    :parameter new: The new values found in the leaf
    :type new: str
    :parameter path:    The json-instance-path leading up
                        to the leaf of which the value is being compared
    :type path: str
    :parameter r_exclude:   Regex to exclude any leafs whose name matches
                            this regular expression
    :type r_exclude: str
    """
    # Used to display the value between two XPATHs
    for key in ref:
        # Case where a context was deleted
        if key not in new:
            print(path + "/" + str(key) + " *** removed ***  ")
    for key in new:
        # Case where a context was created
        if key not in ref:
            print(path + "/" + str(key) + " *** added ***  ")
            printTree(new[key])
        else:
            if new[key] == ref[key]:
                # case where a context already existed and wasn't changed
                pass
            elif isinstance(new[key], (Container, dict)):
                # Case where a context was changed but already existed
                # Not reaching a leaf node -> recursive call to dict_diff
                dict_diff(ref[key], new[key], path + "/" + str(key), r_exclude)
            else:
                # Reached a leaf -> Display the result if the xpath to reach it
                # doesn't match the exclude provided regex
                leaf_diff(path, key, new[key], r_exclude)


def config_ntp(node_handle, arguments):
    # Case where a show command is monitored
    ntp_servers = arguments["xpath"]
    #print(">>",ntp_servers,"<<")
    ip_prefix_array = check_ip_prefixes(ntp_servers)

    if ip_prefix_array is not None:
        configure_ntp_prefix(ip_prefix_array, node_handle)
    else:
        print("Error in format: ", ip_prefix_array)    


def configure_ntp_prefix(ip_prefix_array, connection):
    cfg_path = '/nokia-conf:configure/policy-options'

    for ip_prefix in ip_prefix_array:
        cfg_payload = {
                "nokia-conf:prefix-list": {
                    "name" : "ntp server list",
                    "nokia-conf:prefix": {
                        "nokia-conf:ip-prefix": ip_prefix,
                        "nokia-conf:type": "exact"
                    }              

                }
        }       
        connection.candidate.set(cfg_path,cfg_payload)
        print("Adding prefix to policy-options prefix-list 'ntp server list': ", ip_prefix)

    cfg_path = '/nokia-conf:configure/filter/match-list'
    
    for ip_prefix in ip_prefix_array:
        cfg_payload = {
                "nokia-conf:ip-prefix-list": {
                    "prefix-list-name" : "ntp server list",
                    "nokia-conf:prefix": {
                        "nokia-conf:ip-prefix": ip_prefix
                    }              
                }
        }       
        connection.candidate.set(cfg_path,cfg_payload)
        print("Adding prefix to filter match-list ip-prefix-list 'ntp server list': ", ip_prefix)        

def remove_brackets_and_spaces(input_str):
    # Remove the opening and closing brackets
    input_str = input_str.replace("{", "").replace("}", "")
    
    # Remove any spaces in the string
    input_str = input_str.replace(" ", "")
    
    return input_str

def check_ip_prefixes(input_str):
    # Split the input string into individual IP prefixes
    tmp_str = remove_brackets_and_spaces(input_str)
    prefixes = [prefix.strip() for prefix in tmp_str.split(",")]
    
    # Check if each IP prefix is in the correct format
    valid_prefixes = []
    for prefix in prefixes:
        parts = prefix.split("/")
        if len(parts) != 2:
            print("failed indentifying parts")
            print("Error: Invalid IP prefix format. The correct format is: IP_address/mask_bits")
            return []
        
        try:
            ip_address = parts[0]
            mask_bits = int(parts[1])
            octets = ip_address.split(".")
            if len(octets) != 4:
                print("failed indentifying octects")                
                raise ValueError()
            for octet in octets:
                if not (0 <= int(octet) <= 255):
                    print("failed indentifying every octect")                    
                    raise ValueError()
            if not (0 <= mask_bits <= 32):
                print("failed indentifying mask")
                raise ValueError()
            valid_prefixes.append(prefix)
        except ValueError:
            print("Error: Invalid IP prefix format. The correct format is: IP_address/mask_bits")
            return []
    
    return valid_prefixes
    

def main():
    """The main procedure.  The execution starts here."""
    args = ArgumentHelper()
    args.add_argument(
        "-a",
        Argument(
            "add prefix",
            simple_string,
            "adding prefix to the prefix list 'ntp server list'",
            1,
            None,
        ),
    )

    if found_arguments := args.parse_argv(sys.argv):
        if "helped" in found_arguments.keys():
            return

        # Connect to the node
        node_handle = get_connection()
        config_ntp(node_handle, found_arguments)
    else:
        print("Error while parsing args")


if __name__ == "__main__":
    main()
