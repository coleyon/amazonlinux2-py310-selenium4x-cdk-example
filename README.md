Sample CDK Stack running selenium 4.x on Amazonlinux2

# Dev Environment

```bash
$ docker --version
Docker version 20.10.21, build baeda1f
$ cdk --version
2.121.1 (build d86bb1a)
$ python -V
Python 3.10.12
$ poetry -V
Poetry (version 1.7.1)
$ uname -r
5.10.16.3-microsoft-standard-WSL2
$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 20.04 LTS
Release:        20.04
Codename:       focal
$ node --version
v18.19.0
$ $ poetry show selenium
 name         : selenium 
 version      : 4.16.0   
 description  :
...
$ 
```

# Quick Start

```bash
$ poetry install
$ poetry shell
$ cdk deploy
...
 ✅  SeleniumTestStack

✨  Deployment time: 82.83s

Stack ARN:
arn:aws:cloudformation:xxxxx:xxxxxxx:stack/SeleniumTestStack/xxxxx

✨  Total time: 88.4s
$
```

Now, if we test run the deployed Lambda on the AWS console, you can see that the title of the Google search results page for the keyword 'test' is output to Cloudwatch Logs.

```log
START RequestId: xxxxx Version: $LATEST
...
2024-01-14 03:28:37,620 - libs.selenium - INFO - WebDriver initialized.
2024-01-14 03:28:41,402 - local_debug - INFO - Crawled page title is test - Google Search
END RequestId: xxxx
REPORT RequestId: xxxx Duration: 6897.54 ms Billed Duration: 7814 ms Memory Size: 1024 MB Max Memory Used: 417 MB Init Duration: 916.39 ms
```
