#  Serverless Contact Website Using Amazon S3 & CloudFront

This project demonstrates how to deploy a **static website** with **HTML, CSS, and JavaScript** on **Amazon S3** and deliver it securely and globally using **Amazon CloudFront**. The website includes a simple contact form UI and showcases how static hosting can be made fast, scalable, and cost-effective using AWS services.

##  Features

- Fully static frontend hosted on **Amazon S3**
- Global and secure content delivery via **Amazon CloudFront**
- Custom-designed UI for entering and displaying contact information
- Responsive design that works well on desktop and mobile
- Supports HTTPS and optimized for fast loading

##  Architecture
User ↔️ CloudFront CDN ↔️ Amazon S3 (Static Website Hosting)


- Amazon S3 stores and serves your HTML, CSS, JS files.
- Amazon CloudFront sits in front and caches your content on edge locations globally.
- CloudFront provides an **HTTPS endpoint** (SSL-enabled) for secure access.

## 🧰 Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript
- **Hosting:** Amazon S3 (Static Website Hosting)
- **CDN & SSL:** Amazon CloudFront

##  Why CloudFront?

Amazon S3 static websites don’t natively support HTTPS. By using CloudFront:
- You enable **SSL encryption (HTTPS)**
- You ensure **faster load times** via global edge caching
- You reduce latency and increase reliability

##  Setup Instructions

1. **Upload your static files to an S3 bucket**
   - Enable **Static Website Hosting** in S3
   - Set permissions to allow public read access

2. **Create a CloudFront Distribution**
   - Use your S3 website URL as the origin
   - Enable SSL (default or custom domain)
   - Wait for distribution deployment

##  Live Demo

>  **S3 Website Link:** [http://serverless-contact-site.s3-website-us-east-1.amazonaws.com/)

>  **CloudFront Link:** _(Once CloudFront is set up, you’ll get a secure HTTPS URL like:)_  
> https://diy2zeysap717.cloudfront.net/







