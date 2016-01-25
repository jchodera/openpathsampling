"""

@author: JD Chodera
@author: JH Prinz
"""

import abc

from openpathsampling.netcdfplus import StorableObject, lazy_loading_attributes

import features


# =============================================================================
# ABSTRACT SNAPSHOT (IMPLEMENTS ONLY REVERSED SNAPSHOTS)
# =============================================================================

@lazy_loading_attributes('_reversed')
class AbstractSnapshot(StorableObject):
    """
    Simulation snapshot. Contains references to a configuration and momentum
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, topology=None):
        """
        Attributes
        ----------
        topology : openpathsamping.Topology, default: None
            The corresponding topology used with this Snapshot. Can also be None
            and means no topology is specified.
        """

        super(AbstractSnapshot, self).__init__()

        self._reversed = None
        self.topology = topology

    def __eq__(self, other):
        # This implements comparison with potentially lazy loaded snapshots
        if self is other:
            return True
        elif hasattr(other, '_idx'):
            if other.__subject__ is self:
                return True

        return False

    @property
    def reversed(self):
        """
        Get the reversed copy.

        Snapshots exist in pairs and this returns the reversed counter part.
        No actual velocities are changed. Only if you ask for the velocities of
        a reversed object the velocities will be multiplied by -1.
        """
        if self._reversed is None:
            self._reversed = self.create_reversed()

        return self._reversed

    # ==========================================================================
    # Utility functions
    # ==========================================================================

    @abc.abstractmethod
    def copy(self):
        """
        Returns a shallow copy of the instance itself. The contained
        configuration and momenta are not copied.

        Returns
        -------
        :class:`openpathsampling.AbstractSnapshot`
            the shallow copy

        Notes
        -----
        Shallow here means that content will not be copied but only referenced. Hence
        if you store the shallow copy it will be stored under a different idx, but the
        content (e.g. Configuration object) will not.

        """
        this = self.__class__.__new__(self.__class__)
        AbstractSnapshot.__init__(this, topology=self.topology)
        return this

    def create_reversed(self):
        this = self.copy()
        this._reversed = self
        return this


class FeatureSnapshot(AbstractSnapshot):
    def copy(self):
        return super(FeatureSnapshot, self).copy()


@features.base.set_features(
    features.velocities,
    features.coordinates,
    features.xyz,
    features.topology
)
class ToySnapshot(FeatureSnapshot):
    """
    Simulation snapshot. Only references to coordinates and velocities
    """


@features.base.set_features(
    features.velocities,
    features.coordinates,
    features.box_vectors,
    features.xyz,
    features.topology
)
class MDSnapshot(FeatureSnapshot):
    """
    A fast MDSnapshot
    """


@features.base.set_features(
    features.configuration,
    features.momentum,
    features.xyz,
    features.topology  # for compatibility
)
class Snapshot(FeatureSnapshot):
    """
    The standard MDSnapshot supporting coordinate, velocities and box_vectors
    """
