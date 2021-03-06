# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Define relation between Mementos and buckets."""

from __future__ import absolute_import

from invenio_db import db
from invenio_files_rest.models import Bucket
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import validates
from sqlalchemy_utils.types import UUIDType


class MementoArchives(db.Model):
    """Relationship between Memento and Buckets."""

    __tablename__ = 'memento_archives'

    archived = db.Column(
        db.DateTime,
        primary_key=True,
    )
    """The archivation date and time."""

    key = db.Column(
        db.Text().with_variant(mysql.VARCHAR(255), 'mysql'),
        primary_key=True,
    )
    """Key identifying the archived object."""

    bucket_id = db.Column(
        UUIDType,
        db.ForeignKey(Bucket.id),
        nullable=False,
    )
    """The bucket with archived files related to the ``key``.

    .. note:: There must be a ``ObjectVersion`` with same key.
    """

    bucket = db.relationship(Bucket)

    def __repr__(self):
        """Return representation of Memento."""
        return '{0.archived}/{0.key}:{0.bucket_id}'.format(self)

    @validates('archived')
    def validate_archived(self, key, value):
        """Remove microseconds from the value."""
        return value.replace(microsecond=0) if value else value
