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

# todo try import
from pyHS100 import SmartPlug

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
        item_name_list = item_name.split(',')

        for ip in item_name_list:
          try:
            plug = SmartPlug(ip)
            if plug.state == "OFF":
                plug_state = "Off"
                opposite_state = "On"
            else:
                opposite_state = "Off"
                plug_state = "On\nSince TODO\nCurrent Consumption " + str(plug.current_consumption()) + " W"
            data = {'new_name': 'Turned ' + opposite_state + ' ' +  plug.alias + '!'}
            items.append(ExtensionResultItem(icon='images/icon.png',
                                               name='Smart Plug %s' % (plug.alias),
                                               description='Current State %s\n\nModel %s\nIP %s' % (plug_state, plug.model, ip),
                                               on_enter=ExtensionCustomAction(data, keep_app_open=True)))
          except:
            plug_state = "Can't reach the plug %s. Verify the IP address." % ip
            data = {'new_name': '%s was clicked' % plug}
            items.append(ExtensionResultItem(icon='images/icon.png',
                                               name='Smart Plug %s' % (plug.alias),
                                               description='Current State %s\n\nModel %s\nIP %s' % (plug_state, plug.model, ip),
                                               on_enter=ExtensionCustomAction(data, keep_app_open=True)))


        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=data['new_name'],
                                                           on_enter=HideWindowAction())])


if __name__ == '__main__':
    DemoExtension().run()
