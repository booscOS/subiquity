# Copyright 2015 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Hostname

Sets system hostname

"""
import logging
from urwid import (Pile, Columns, Text, ListBox)
from subiquity.ui.buttons import done_btn, cancel_btn
from subiquity.ui.interactive import StringEditor
from subiquity.ui.utils import Padding, Color
from subiquity.view import ViewPolicy

log = logging.getLogger("subiquity.views.hostname")


class HostnameView(ViewPolicy):
    def __init__(self, model, signal):
        self.model = model
        self.signal = signal
        self.hostname = StringEditor(caption="")

        body = [
            Padding.center_50(self._build_model_inputs()),
            Padding.line_break(""),
            Padding.center_15(self._build_buttons()),
        ]
        super().__init__(ListBox(body))

    def _build_buttons(self):
        cancel = cancel_btn(label=_("Cancel"), on_press=self.cancel)
        done = done_btn(label=_("Done"), on_press=self.done)

        buttons = [
            Color.button(done, focus_map='button focus'),
            Color.button(cancel, focus_map='button focus')
        ]
        return Pile(buttons)

    def _build_model_inputs(self):
        sl = [
            Columns(
                [
                    ("weight", 0.2, Text(_("Hostname"), align="right")),
                    ("weight", 0.3,
                     Color.string_input(self.hostname,
                                        focus_map="string_input focus"))
                ],
            )
        ]
        return Pile(sl)

    def done(self, result):
        result = {
            "hostname": self.hostname.value
        }

        self.signal.emit_signal('hostname:finish', result)

    def cancel(self, button):
        self.signal.emit_signal(self.model.get_previous_signal)
