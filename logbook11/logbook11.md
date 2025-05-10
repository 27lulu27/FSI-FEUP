PKI SEEDLABS

labsetup

![](1.png)

Task 1: Becoming a Certificate Authority (CA)

 - uncomment “unique_subject” line 
 - created index.txt and serial files
 - issue self-signed certificate
![](2.png)
![](3.png)

What part of the certificate indicates this is a CA’s certificate?

CA: TRUE
![](4.png)

What part of the certificate indicates is a self-signed certificate?
issuer == subject
![](5.png)

In the RSA algorithm, we have a public exponent e, a private exponent d, a modulus n, and two secret numbers p and q, such that n = pq. Please identify the values for these elements in your certificate and key files

in ca.crt
![](7.png)
Exponent: 65537 (0x10001)

in ca.key
![](8.png)


Task 2: Generating a Certificate Request for Your Web Server

![](6.png)

our domains
www.l10g0724.com
www.l10g072425.com
www.l10g072024.com

Task 3: Generating a Certificate for your server

we turned csr into a certificate using CA. CA is false unlike self-signed

![](9.png)

the Subject Alternative Name field, we can see that the alternative names are included in the certificate

Task 4: Deploying Certificate in an Apache-Based HTTPS Website

our HTTPS website www.l10g07.com
 - created l10g07_apache_ssl.conf in /etc/apache2/sites-available/

![](10.png)

 - moved server.crt and server.key to /volumes/
 - ran a2ensite l10g07_apache_ssl
 - start apache server in container

![](11.png)

 - after importing the ca certificate we were able to access our domain

![](12.png)

Task 5:  Launching a Man-In-The-Middle Attack


