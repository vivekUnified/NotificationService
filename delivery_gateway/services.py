import logging

logger = logging.getLogger(__name__)

class BaseChannelService:
    def send(self, destination, content):
        raise NotImplementedError

class EmailService(BaseChannelService):
    def send(self, destination, content):
        logger.info(f"[Email] Sending to {destination}: {content}")
        # Add actual email sending logic here
        return True

class SlackService(BaseChannelService):
    def send(self, destination, content):
        logger.info(f"[Slack] Sending to {destination}: {content}")
        # Add Slack API logic here
        return True

class InAppService(BaseChannelService):
    def send(self, destination, content):
        logger.info(f"[In-App] Pushing to {destination}: {content}")
        return True

class TeamsService(BaseChannelService):
    def send(self, destination, content):
        logger.info(f"[Teams] Sending to {destination}: {content}")
        return True

class ChannelFactory:
    @staticmethod
    def get_service(channel):
        if channel == 'email':
            return EmailService()
        elif channel == 'slack':
            return SlackService()
        elif channel == 'in_app':
            return InAppService()
        elif channel == 'teams':
            return TeamsService()
        return None
