"""A simple MQTT client
"""

import sys
import logging
import click
import paho.mqtt.client as mqtt
from paho.mqtt.publish import single

from click_mqtt import __version__

__author__ = "Oliver van Porten"
__copyright__ = "Oliver van Porten"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

DEFAULT_TOPIC = '/demo'

@click.group()
@click.option('-b', '--broker',
              help='The broker to send to/read from',
              default='http://localhost:1883',
              show_default=True)
@click.pass_context        
def cli(ctx, broker=None):
    ctx.ensure_object(dict)   
    click.echo(click.style('Using broker {}'.format(broker),
                fg='green'))
    ctx.obj['BROKER'] = broker

@cli.command()
@click.option('--topic',
            help='Topic to subscribe to',
            default=DEFAULT_TOPIC)
@click.pass_context
def read(ctx, topic=None):
    """Subscribe to a single topic, 
       read a single message and print it
    """
    def on_connect(client, userdata, flags, rc):
        click.echo ('Connected: {}'.format(str(rc)))
        client.subscribe(topic)
    def on_message(client,userdata, msg):
        click.echo('{}: {}'.format(msg.topic, msg.payload))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(ctx.obj['BROKER'], port=1883, keepalive=60)
    client.loop_forever()

@cli.command()
@click.option('-t', '--topic',
              help='The topic',
              default=DEFAULT_TOPIC,
              show_default=True)
@click.option('-m', '--message',
              help='The message',
              required=True)
@click.pass_context
def write(ctx, topic, message):
    """Publish a single message to
       a given topic"""
    
    
    ''' https://pypi.org/project/paho-mqtt/#publishing
    single(topic, payload=None, qos=0, retain=False, hostname="localhost",
    port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
    protocol=mqtt.MQTTv311, transport="tcp")
    '''
    single(topic, payload=message, hostname=ctx.obj['BROKER'], retain=True)
    

if __name__ == "__main__":
    cli(obj={})
