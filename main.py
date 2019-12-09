import json
import logging
from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

# TODO autodiscovery. Autodiscovery doesn't work for me, probably because my subnet is too large.
import socket
import datetime

logger = logging.getLogger(__name__)

class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        logger.info('preferences %s' % json.dumps(extension.preferences))
        item_name = extension.preferences['ip']
        item_name_list = item_name.split(' ')

        try:
            from pyHS100 import SmartPlug
        except:
            logger.info('Python library missing.')
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='Python library pyHS100 missing. See extension README.',
                                             on_enter=ExtensionCustomAction('Nothing I can do for you.',
                                             keep_app_open=False)))
        else:
            for ip in item_name_list:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, int(9999)))
                    s.shutdown(2)
                    plug = SmartPlug(ip)

                    plug_name = plug.hw_info['dev_name']

                    if plug.state == "OFF":
                        plug_state = "OFF"
                        opposite_state = "On"
                    elif plug.state == "ON":
                        plug_since = plug.on_since
                        now = datetime.datetime.now()
                        diff = now - plug_since
                        diff_display = diff.seconds / 60
                        plug_state = "ON\nFor " + str(int(diff_display)) + " minutes (Current Consumption " + str(plug.current_consumption()) + " w)"
                        opposite_state = "Off"

                    data = {'new_name': 'Turning ' + opposite_state + ' ' + plug.alias + '!',
                            'target': ip, 
                            'desired_state': opposite_state}

                    items.append(ExtensionResultItem(icon='images/icon.png',
                                                    name='Smart Plug %s' % (plug.alias),
                                                    description='%s - %s\n\nCurrent State %s\nIP %s' % (plug_name, plug.model, plug_state, ip),
                                                    on_enter=ExtensionCustomAction(data, keep_app_open=True)))

                except:
                    logger.info('Failed to communicate with device.')

                    data = {'new_name': 'Failed to communicate with Smart Plug ' + plug.alias
                           }

                    items.append(ExtensionResultItem(icon='images/icon.png',
                                                    name='Smart Plug %s is not reachable.' % ip,
                                                    on_enter=ExtensionCustomAction(data, keep_app_open=False)))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):

        from pyHS100 import SmartPlug

        data = event.get_data()
        logger.info(data)
        plug = SmartPlug(data['target'])

        if data['desired_state'] == "On":
            plug.turn_on()
        elif data['desired_state'] == "Off":
            plug.turn_off()

        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=data['new_name'],
                                                           on_enter=HideWindowAction())])


if __name__ == '__main__':
    DemoExtension().run()
