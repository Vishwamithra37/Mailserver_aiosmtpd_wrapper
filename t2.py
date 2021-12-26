
import asyncio
from asyncio.base_events import Server
import logging
import aiosmtpd
from aiosmtpd.controller import DEFAULT_READY_TIMEOUT, Controller
import ssl
from aiosmtpd.smtp import SMTP, Envelope, Session
from smtplib import SMTP as SMTPCLient
import dns.resolver

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain('cert.pem', 'privkey.pem')


def get_mx(domain):
    records = dns.resolver.resolve(domain, "MX")
    if not records:
        return None
    records = sorted(records, key=lambda r: r.preference)
    print(records)
    return str(records[0].exchange)

class ExampleHandler():
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        print('RCPT to %s' % address)
        # Accet emails from galam.in and gmail.com.
        if not address.endswith('@galam.in') and not address.endswith('@gmail.com'):
            print('not Recieving')
            return '550 Not my domain'
        envelope.rcpt_tos.append(address)
        print(address+" "+"is added to rcpt_tos")
      

        # Make an envelope for the recipient with the same content.
        
        
        
        return '250 The message will not go further than this point to the recipient'


    async def handle_DATA(self, server, session, envelope):
        # if not envelope.mail_from.endswith('@reddit.com'):
        #     print('Pingpong failure')
        #     return '550 no Such reciever'
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:\n')
        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
            print(f'> {ln}'.strip())
        print()
        print('End of message')
        # Dump the contents of envelope.content to a file.
        fi=open('./mailbox/firstletter.txt','w')
        fi.write(envelope.content.decode('utf8', errors='replace'))
        fi.close()

        mx_rcpt = {}
        for rcpt in envelope.rcpt_tos:
            _, _, domain = rcpt.partition("@")
            mx = get_mx(domain)
            if mx is None:
                continue
            mx_rcpt.setdefault(mx, []).append(rcpt)

        for mx, rcpts in mx_rcpt.items():
            kk=(25,587,465)
            for gk in kk:
             try:
                with SMTPCLient(mx, gk) as client:
                    client.sendmail(
                        from_addr=envelope.mail_from,
                        to_addrs=rcpts,
                        msg=envelope.original_content
                    )
                    print("Successfully sent email to %s" % rcpts)
                    return '250 The message will not go further than this point to the recipient'
            # Print the error if something goes wrong.
             except Exception as e:
                print(e)
                continue
        return ('550 Could not send email to %s' % rcpts)

            


        
    #Define Relay server.
  



async def amain(loop):
    cont = Controller(ExampleHandler(),hostname='192.168.1.33', port=587,tls_context=context, server_hostname='Galam Limited',ready_timeout=5000) 
    # Combining ExampleHandler and Controller into a single Controller.
   
    cont.start()


if __name__ == '__main__':
    # log debug messages to stdout.
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    loop.create_task(amain(loop=loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
  
    
