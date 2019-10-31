# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 HERE Europe B.V.
#
# SPDX-License-Identifier: MIT
# License-Filename: LICENSE
#
###############################################################################

from qgis.PyQt.QtWidgets import QDialog
from . import get_ui_class

from ..models.token_model import GroupTokenInfoModel
from .util_dialog import ConfirmDialog
from .token_info_dialog import NewTokenInfoDialog, EditTokenInfoDialog
from qgis.PyQt.QtGui import QStandardItem

TokenUI = get_ui_class('token_dialog.ui')

class TokenDialog(QDialog, TokenUI):
    title="Token Manager"
    def __init__(self, parent=None):
        """init window"""
        QDialog.__init__(self, parent)
        TokenUI.setupUi(self, self)
        self.setWindowTitle(self.title)

    def config(self, token_model: GroupTokenInfoModel):
        
        self.token_model = token_model

        self.tableView.setModel( token_model)
        self.tableView.setSelectionMode(self.tableView.SingleSelection)
        self.tableView.setSelectionBehavior(self.tableView.SelectRows)
        self.tableView.setEditTriggers(self.tableView.NoEditTriggers)

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(header.ResizeToContents)

        self.btn_add.clicked.connect( self.ui_add_token)
        self.btn_edit.clicked.connect( self.ui_edit_token)
        self.btn_delete.clicked.connect( self.ui_delete_token)
        # self.btn_up.clicked.connect()
        # self.btn_down.clicked.connect()
    def _get_current_token_info(self):
        row = self.tableView.currentIndex().row()
        return self.token_model.get_token_info(row)
    def ui_add_token(self):
        dialog = NewTokenInfoDialog(self)
        dialog.accepted.connect(lambda: self._add_token(
            dialog.get_token_info()
        ))
        dialog.exec_()

    def ui_edit_token(self):
        dialog = EditTokenInfoDialog(self)
        dialog.set_token_info(self._get_current_token_info())
        dialog.accepted.connect(lambda: self._edit_token(
            dialog.get_token_info()
        ))
        dialog.exec_()

    def ui_delete_token(self):
        row = self.tableView.currentIndex().row()
        token_info = self.token_model.get_token_info(row)
        token_msg = ", ".join("%s: %s"%it for it in token_info.items())
        dialog = ConfirmDialog("Do you want to Delete token (%s)?"%token_msg)
        ret = dialog.exec_()
        if ret != dialog.Ok: return

        self.token_model.takeRow(row)
        
    def _add_token(self, token_info: dict):
        self.token_model.appendRow([
            QStandardItem(token_info["name"]),
            QStandardItem(token_info["token"])
        ])
    
    def _edit_token(self, token_info: dict):
        row = self.tableView.currentIndex().row()
        self.token_model.setItem(row, 0,
        QStandardItem(token_info["name"]))
        self.token_model.setItem(row, 1,
        QStandardItem(token_info["token"]))
