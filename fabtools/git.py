"""
Git
===

This module provides low-level tools for managing `Git`_ repositories.  You
should normally not use them directly but rather use the high-level wrapper
:func:`fabtools.require.git.working_copy` instead.

.. _Git: http://git-scm.com/

"""

from __future__ import with_statement

from fabric.api import run
from fabric.api import sudo
from fabric.context_managers import cd

from fabtools.utils import run_as_root


def clone(remote_url, path=None, use_sudo=False, user=None):
    """ Clone a remote Git repository into a non existing directory.

    :param remote_url: URL of the remote repository to clone.
    :type remote_url: str

    :param path: Path of the working copy directory.  Must not exist yet.
    :type path: str

    :param use_sudo: If ``True`` execute ``git`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    """

    cmd = 'git clone --quiet %s' % remote_url
    if path is not None:
        cmd = cmd + ' %s' % path

    if use_sudo and user is None:
        run_as_root(cmd)
    elif use_sudo:
        sudo(cmd, user=user)
    else:
        run(cmd)


def pull(path, use_sudo=False, user=None, stash=False):
    """ Pull from a remote Git repository on an existing working copy.

    :param path: Path of the working copy directory.  This directory must exist
                 and be a Git working copy with a default remote to pull from.
    :type path: str

    :param use_sudo: If ``True`` execute ``git`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.

    :type stash: bool
    :param stash: If ``stash is True``, run git stash first.

    :type user: str
    """

    if path is None:
        raise ValueError("Path to the working copy is needed to pull from a "
                         "remote repository.")

    cmd = 'git pull'
    if stash:
      cmd = "(git stash; %s)" % cmd

    with cd(path):
        if use_sudo and user is None:
            run_as_root(cmd)
        elif use_sudo:
            sudo(cmd, user=user)
        else:
            run(cmd)


def checkout(path, branch="master", use_sudo=False, user=None):
    """ Checkout an existing branch of an existing Git working copy.

    :param path: Path of the working copy directory.  This directory must exist
                 and be a Git working copy.
    :type path: str

    :param branch: Name of the branch to checkout.
    :type branch: str

    :param use_sudo: If ``True`` execute ``git`` with
                     :func:`fabric.operations.sudo`, else with
                     :func:`fabric.operations.run`.
    :type use_sudo: bool

    :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                 with the given user.  If ``use_sudo is False`` this parameter
                 has no effect.
    :type user: str
    """

    if path is None:
        raise ValueError("Path to the working copy is needed to checkout a "
                         "branch")

    cmd = 'git checkout %s' % branch

    with cd(path):
        if use_sudo and user is None:
            run_as_root(cmd)
        elif use_sudo:
            sudo(cmd, user=user)
        else:
            run(cmd)
