# --------------------------------------------------------
# (c) Copyright 2014, 2020 by Jason DeLaat.
# Licensed under BSD 3-clause licence.
# --------------------------------------------------------
""" Implements the Maybe monad and related functions.

The Maybe monad is used to represent calculations that may or may not
return a value. Alternately, if used as function inputs, Maybe values
can be used to indicate 'optional' inputs, explicitly passing
'Nothing' when no input is required.

When creating Maybe values directly use the 'Just' function or 'Nothing':

  Example:
    x = Just(19)
    y = Just('A string')
    z = Nothing

The 'insert' class method is a wrapper around the 'Just' function.

  Example:
    x = Maybe.insert(9) # Same as Just(9)
"""

import pymonad.monad

class Maybe(pymonad.monad.Monad):
    """ The Maybe monad class. """
    @classmethod
    def insert(cls, value):
        """ See Monad.insert """
        return Just(value)

    def amap(self, monad_value):
        """ See Monad.amap"""
        if self.is_nothing() or monad_value.is_nothing(): #pylint: disable=no-else-return
            return Nothing
        else:
            return monad_value.map(self.value)

    def bind(self, kleisli_function):
        """ See Monad.bind """
        if self.monoid is False: #pylint: disable=no-else-return
            return self
        else:
            try:
                return kleisli_function(self.value)
            except: # pylint: disable=bare-except
                return Nothing

    def is_just(self):
        """ Returns True if the monad instance was created with the 'Just' function. """
        return self.monoid

    def is_nothing(self):
        """ Returns True if the monad instance is the 'Nothing' value. """
        return not self.monoid

    def map(self, function):
        """ See Monad.map """
        if self.is_nothing(): #pylint: disable=no-else-return
            return self
        else:
            try:
                return Just(function(self.value))
            except: # pylint: disable=bare-except
                return Nothing

    def __eq__(self, other):
        """ Checks equality of Maybe objects.

        Maybe objects are equal iff:
          1. They are both Nothing, or
          2. They are both Just and
            2a. They both contain the same value.
        """
        return self.value == other.value and self.monoid == other.monoid

    def __repr__(self):
        return f'Just {self.value}' if self.monoid else 'Nothing'

def Just(value): # pylint: disable=invalid-name
    """ A Maybe object representing the presence of an optional value. """
    return Maybe(value, True)

# A Maybe object representing the absence of an optional value.
Nothing = Maybe(None, False) # pylint: disable=invalid-name







class Option(pymonad.monad.MonadAlias, Maybe): # MonadAlias must be the first parent class
    """ An alias for the Maybe monad class. """
    def __repr__(self):
        return f'Some {self.value}' if self.monoid else 'Nothing'

def Some(value): # pylint: disable=invalid-name
    """ An Option object representing the presence of an optional value. """
    return Option(value, True)
