# Mailserver_aiosmtpd_wrapper
So, You wanted to make a mail server in python? Great. You are at the right place!

**A brief intro to SMTP:**
<ol>
<li>
 <b>SMTP</b>- Simple Mail Transfer Protocol, has <b>only one job to do. That is to pass the mail enevelope from one device to another device. This can be from user to server or server to server. Implemented by SMTPlib library. </b>
  
</li>
  <li>
   <b> A Mail server </b>is nothing but a place where Mails reside. That is, Mails come and sit there from various sources (Other email servers/users implmenting SMTP). The Mail server is simply responsible for handling security handshakes and to-from verifications of the email. The mail server uses the port 25, 465, 587, 2525 or any other custom port. And to this port and the IP address is where the SMTP protocol sends the Mails. 
    
  </li>
</ol>

**AIOSMTPD and SMTPlib**

The AIOSMTPD library provides a library to implement a **Mail server**, and the **SMTPlib** library is capable of implementing the smtp protocol.

**A stupid understanding of SMTP in real world**

At its core, SMTP is simply a tcp based application which sends E-mail to whoever is specified in the **SMTP.send (In python)**. In essence, all it needs is an address(IP:port) to send the email specified in the envelope. 

**An simple letter exchange with AIOSMTPD server and Gmail server**






