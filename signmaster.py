from ledsign.minisign import MiniSign
def sendmessage(message):
    mysign=MiniSign(
        devicetype='sign',
        port='/dev/ttyUSB0'
        )
    for line in message:
        mysign.queuemsg(
            data=line,
            speed=3,
            effect='hold'
            )
    mysign.sendqueue(
        device='/dev/ttyUSB0'
        )
