# pylint: disable=broad-except, attribute-defined-outside-init
from __future__ import annotations

import logging
from typing import Union

from payments.domain import commands, events
from payments.service_layer import handlers

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


def handle(message: Message):
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, events.Event):
            handle_event(message)
        elif isinstance(message, commands.Command):
            handle_command(message)
        else:
            raise Exception(f"{message} was not an Event or Command")


def handle_event(
        event: events.Event,
):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            logger.debug("handling event %s with handler %s", event, handler)
            handler(event)
        except Exception:
            logger.exception("Exception handling event %s", event)
            continue


def handle_command(
        command: commands.Command,
):
    logger.debug("handling command %s", command)
    try:
        handler = COMMAND_HANDLERS[type(command)]
        handler(command)
    except Exception:
        logger.exception("Exception handling command %s", command)
        raise


COMMAND_HANDLERS = {
    commands.PayByCreditCard: handlers.pay_by_credit_card,
}  # type: Dict[Type[commands.Command], Callable]


EVENT_HANDLERS = {

}  # type: Dict[Type[events.Event], List[Callable]]
