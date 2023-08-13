#!/usr/bin/python3

"""Class for AirBnB clone console."""

import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage

classes = {"BaseModel": BaseModel,
           "User": User,
           "State": State,
           "City": City,
           "Amenity": Amenity,
           "Place": Place,
           "Review": Review
           }


class HBNBCommand(cmd.Cmd):
    """ Implement HBNB class."""
    prompt = "(hbnb) "

    def do_quit(self, line):
        """Quit command to exit the program"""
        exit()

    def help_quit(self):
        """help for the quit command."""
        print("Quit command to exit the program\n")

    def do_EOF(self, line):
        """handle end-of-file marker"""
        return True

    def help_EOF(self):
        """help for EOF."""
        print("handles end-of-file marker\n")

    def emptyline(self):
        """Handle when no input is given"""
        pass

    def help_emptyline(self):
        """Help for emptyline."""
        print("Handles when no input is given (Space and 'Enter' is passed)\n")

    def do_create(self, line):
        """Create a new instance of BaseModel."""
        if line:
            tokens = line.split()
            if len(tokens) < 1:
                print("** class name missing **")
            else:
                class_name = tokens[0]
                instance = None

                for key, val in classes.items():
                    if class_name.lower() == key.lower():
                        instance = val()
                        break

                if instance is None:
                    print("** class doesn't exist **")
                else:
                    print(instance.id)
                    instance.save()
        else:
            print("** class name missing **")

    def help_create(self):
        """help for 'create()'."""
        print("Creates a new instance of given class and prints its id\n")

    def do_show(self, line):
        """Prints string repr. of an instance based on the class name and id"""
        if line:
            tokens = line.split()
            if len(tokens) < 2:
                if len(tokens) < 1:
                    print("** class name missing **")
                elif len(tokens) == 1:
                    if tokens[0] not in classes:
                        print("** class doesn't exist **")
                        return
                    print("** instance id missing **")
            else:
                flag = False
                full_id = f"{tokens[0]}.{tokens[1]}"
                objects = storage.all()

                for key, val in classes.items():
                    if tokens[0].lower() == key.lower():
                        flag = True
                        break

                if not flag:
                    print("** class doesn't exist **")
                else:
                    if full_id in objects:
                        stripped_obj = objects[full_id]
                        print(stripped_obj)
                    else:
                        print("** no instance found **")
        else:
            print("** class name missing **")

    def do_destroy(self, line):
        """Delete an instance based on the class name and id"""
        if line:
            tokens = line.split()
            if len(tokens) < 2:
                if len(tokens) < 1:
                    print("** class name missing **")
                elif len(tokens) == 1:
                    if tokens[0] not in classes:
                        print("** class doesn't exist **")
                        return
                    print("** instance id missing **")
            else:
                if tokens[0] not in classes:
                    print("** class doesn't exist **")
                    return

                flag = False
                full_id = f"{tokens[0]}.{tokens[1]}"
                objects = storage.all()

                for key, val in classes.items():
                    if tokens[0].lower() == key.lower():
                        flag = True
                        break

                if not flag:
                    print("** class doesn't exist **")
                else:
                    if full_id in objects:
                        del objects[full_id]
                        storage.save()
                    else:
                        print("** no instance found **")
        else:
            print("** class name missing **")

    def do_all(self, line):
        """Prints all string representation of all instances."""
        obj_dict = storage.all()
        tokens = line.split()
        new_list = []
        flag = False

        if tokens:
            for key, instance in obj_dict.items():
                if tokens[0].lower() == instance.__class__.__name__.lower():
                    new_list.append(instance.__str__().replace('"', ''))
                    flag = True
            if not flag:
                print("** class doesn't exist **")
            else:
                print(new_list)
        else:
            for instance in obj_dict.values():
                flag = True
                new_list.append(instance.__str__().replace('"', ''))

            print(new_list)

    def do_update(self, line):
        """Updates an instance based on the class name and id"""
        if line:
            tokens = line.split()

            objects = storage.all()
            if len(tokens) < 4:
                if len(tokens) < 1:
                    print("** class name missing **")
                elif len(tokens) == 1:
                    if tokens[0] not in classes:
                        print("** class doesn't exist **")
                        return
                    print("** instance id missing **")

                elif len(tokens) == 2:
                    full_id = f"{tokens[0]}.{tokens[1]}"
                    if full_id not in objects:
                        print("** no instance found **")
                        return
                    print("** attribute name missing **")

                elif len(tokens) == 3:
                    print("** value missing **")
            else:
                if tokens[0] not in classes:
                    print("** class doesn't exist **")
                    return

                else:
                    full_id = f"{tokens[0]}.{tokens[1]}"
                    if full_id in objects:
                        base_dict = objects[full_id]

                        attr_val = tokens[3].replace('"', '')
                        if tokens[2] in base_dict.__dict__:
                            old_type = type(base_dict.__dict__[tokens[2]])
                            try:
                                converted = old_type(attr_val)
                                base_dict.__dict__[tokens[2]] = converted
                                storage.save()
                            except ValueError:
                                print("** invalid value type **")
                        else:
                            base_dict.__dict__[tokens[2]] = attr_val
                            storage.save()
                    else:
                        print("** no instance found **")
        else:
            print("** class name missing **")

    def default(self, line):
        """Default behavior for console when input is invalid"""
        cmd_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }

        if '.' in line:
            tokens = line.split(".")
            if len(tokens) == 2:
                cmd_args = tokens[1]
                if '(' in cmd_args and ')' in cmd_args:
                    command, arguments = cmd_args.split('(', 1)
                    arguments = arguments.rstrip(')')
                    if command in cmd_dict:
                        call = "{} {}".format(tokens[0], arguments)
                        return cmd_dict[command](call)
                    else:
                        print("*** Unknown syntax: {}".format(line))
                else:
                    print("*** Unknown syntax: {}".format(line))
            else:
                print("*** Unknown syntax: {}".format(line))
        else:
            print("*** Unknown syntax: {}".format(line))
        return False

    def do_count(self, line):
        """Retrieve the number of instances of a class"""
        tokens = line.split()
        objects = storage.all()

        if len(tokens) == 0:
            print("** class name missing **")
            return
        elif tokens[0] not in classes:
            print("** class doesn't exist **")
            return
        else:
            count = 0
            for obj in objects.values():
                if obj.__class__.__name__ == tokens[0]:
                    count += 1
            print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
