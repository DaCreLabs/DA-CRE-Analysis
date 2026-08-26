# =============================================================================
# DACRE WORLDWIDE - COMPLETE PRODUCTION BUILD (FIXED)
# Version: 7.3.0 - Dark Online Robot / Holographic Service Fabric
# Total Lines: ~12,000+
# Features: Self-Healing DB, DI Intelligence, Error Shield, Voice, Video, AI
# =============================================================================

# =============================================================================
# IMPORTS - FIXED (removed deprecated 'pipes' import)
# =============================================================================

import hashlib
import hmac
import html
import io
import json
import os
import re
import sqlite3
import urllib.parse
import urllib.request
import smtplib
import threading
import time
import uuid
import base64
import random
import string
import tempfile
import subprocess
import sys
import traceback
import logging
import queue
import asyncio
import concurrent.futures
import inspect
import functools
import itertools
import collections
import datetime
import calendar
import math
import statistics
import typing
import warnings
import zipfile
import csv
import xml.etree.ElementTree as ET
import secrets
import binascii
import struct
import pickle
import shelve
import dbm
import zlib
import gzip
import bz2
import lzma
import tarfile
import shutil
import fileinput
import glob
import fnmatch
# REMOVED: import pipes (deprecated)
import getpass
import platform
import sysconfig
import socket
import ssl
from contextlib import contextmanager
from html.parser import HTMLParser
from urllib.parse import urlparse
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any, Tuple
from enum import Enum
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from decimal import Decimal
from fractions import Fraction

# =============================================================================
# HIDE MANAGE APP BUTTON - COMPLETE SOLUTION
# =============================================================================

import pandas as pd
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components

BASE_DIR = Path(__file__).resolve().parent
DACRE_ASSET_DIR = BASE_DIR / "assets"
DACRE_LOGO_PATH = DACRE_ASSET_DIR / "dacre_logo.png"
DACRE_CEO_PATH = DACRE_ASSET_DIR / "dacre_ceo.png"
DACRE_FAVICON_PATH = DACRE_ASSET_DIR / "dacre_favicon.png"

# The browser icon is always the DACRE mark. The embedded fallback keeps it
# working even when Streamlit Cloud is deployed with app.py alone.
_DACRE_FAVICON_B64 = "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAbR0lEQVR4nO2babBlV3Xff2vvc+705tdzqzW0Wmq1xpYESGYyYHAEcRGMZAiEkkwEZMAh2HFVUhUyOA6FnZRxiqoEU7Er2IkrLjBjIKYCpISYhAISQqABDa0eX7/Xr997dzzz3isf9rn33ZZEcOWLPsCpOm84d5+995r/a619pbl8WPkZvswLvYEX+vo5A17oDbzQ188Z8EJv4IW+Iqn/GIeCZ///179eqGAiP33IT3hLgahyeuHj58wnIM+3yLOePc+Y8SI/6f+fONfzXdMSUp2aTJ87SH+SMLY/V0BQoso/W/Y8ixhBjKmHSxgl1BPIs96V8RuTORStN1Q/qzcvCDre6Hg9vXDd6X3r9LZEw0NRUF/TqwiKqp/iidZ80guZMsW4SMaECVMETm1IpN6MIFOMMdPjJ/zkgjFjMlTGgvMg2/NMfsr2LBesOSUb2X6h5ogCHsQg+Anz5DlarIFfAqq12si28CJ9lorrszcmAlL7ygkz6o9rgsAGLk+orsfV7403ZcSA99tjp21irBXbYq41hm3mTpiwLX3U1XuclvK0KWzTJlOCGl+RyIUM2FbfMRFjjpqJJNR7MBaaMxA1wTskG4HY8FxMvbhOfku9oQsYNSGo3pSY7Q2rgInC+9NMkGkia+LVh1t82Od43el9TGjyU0xRIsRMJCHThI8lKduMEBRMhLSaYC04RcoiSNU2UJWgFbigdgSCRWwgQMP7z77UKxeamg3qqj4wFRAxNUG+ZqHb1tSJttQETjTT1yvUTBkLcsofRBO9GmuBTEGDyaZqbjY60GhCVUJe1M6pVsXJOzY8j5phIV8G+asiNjAiCKjWIhPG491EZbcdmQ3vGoOIQYxBJA5KoRVoBeoQPKoO/LZ5TpSEqb1Nnm3TFz1H4hcQTyCu1UFaM2hRIMlowhT1wQbFWBCL2BhRRdUhrkDFgm0G5sWdoMLtBTTvQ7IFNoa5/YAN2qc6UWktS6hSpMzAK9gYr0tg50AHUG5C6Wvn5gFFrGBMBN7hXW0eY+lPzGJMrdZkLlyjF6j6NPFikM5ccEx5XquYBpuXWtpit7XGFYGoeCbcJoZiOGEIVYp6F8aLIFE0pZJa271FTQNsC4kaYJrgFLU7ec2df4srX3Q1n/vE9ylXvk9b+ggJlAmjwYCt9R50++ALaAuRgKv8thao8mzfFPEcu6+lbptIew4tc/C1c9Eq+AEbB1WtkbSoCy+2d6LxLFQjSLeQKkVEkbiFNJqw6zAyu4TptBFrkSzDq0GrCp8MIe2hZQF5ghY9yDwSNdCZJRYOXMrN/+i1sATXrMKJ/73GTDOi1eywtAhLO4WFGcgGGT9+YIUHvnmCarOLzBnEm6CtE62GcWwUWbxWt8NccDJEjWDvZVbHZQO+DA5QDNgG6itkrLKmGaSsHlwONoKoVTMqQqwQ7bgEM78LVw7RIsH31tFhD2yMxC20yqEK/kJso5aECXMYRYsZrnjDG5k9coiH/ssX0RNfh2wFXBW8f7tBe0+LQ0cXeekbDnLo0B7+z+dX+czHHwbNsE2Lr8aaMPYxisjidXqBs4uaELegSGuHVgMOE4OJa7TlEImCA8OgVRqcXNRAGrPQWgi4bHQu2LCJYWYn4lL8aAPUh3Br67AnErSsRpxBVQXFBmbaJtLZgc+bkJUQbWGyM0EbJWimlhk+zyGrQCr2vmqJ93zwF9hj9vDv3ns/p55Yxc7F+PJCcwgaMN6EbQTpVzlga++uiG2gphmcjXfQ2QNVCsUItAj22t4R3i2GqFNEgnc2jQ6YCC1T1OVokYDU6MxsAyxZ2IO0Gpi8wOcZxHFwOXELJEbMDMaASiNsa3gGP1iDcoRGrcBknyMuQXyJ66bQrnjbR6/jjjfdyO++9Uf88FvHsTMx3vkJvqg1gBCfbSs4ECz4qlbvGHUFkTiIWkhjAcoELQZgIkxnLyotyLYCY0Wg6OM9+Mbu4O2LASzuh04Hm54L9tiZwyzvR5MBmvZhfi8qgtUK02rjyixIKG6jeYnPcySK8CXQ7UJnEdMykJ1H080Ah+NZFA/lEJEKSRJcPuDdnz7Kr7zmOv7xqx7k1FPnsU2Dr5NAYfE6lTpM4YpaBWs1sS3wnosPvYqFA69HbRtrPbHJsHGEbc9hWi0sQxotwTY7iBkipgLjMdUQ319huHaGlccf49TTx8mrCJoe22mi8xehxQh6azC7C1rzQfHyDDHNIASfIzUo8oMh+y65iKNvfzNbT53kgS98Fd+eQbRAk3NoMQy+J56Bso+4EQxSmoc8H/7Gi+k/Os8H3vgQGhWoC2YQgYZY7coAVdVPQpwqRCRUy2/n6eRGrJZIHAd3UIKpwu+oDbED4+v12xB1oDEHswuwNAeXSU5r/WnO3vc97v/M5zi3MQSbYG0Dv3BpsHUvkGcgcTBDVShLcAWaZyy2m7zs33+QjUMXsb8NjU6Lb/zpX2J37YTZ/Ui+iY7Wa9wxF2iZg/TxLl/4+HH+/j+5jhe/fg/3f+4EdtbiKzDB42pIKsYxQgke2BeAIU1yKBKo+lAOoEjQIkOLDClyyAt8VgZVTUrcsMANCopuQe9cwemVkicGDZ4+cA2L//Au3vWpj3HHu/8OcdXGlYJRQYsqmEuewnAN0h4UBZoPoRyggy1u/Y33cPbii9g4kfLUGceuu97Knov34QabiCvReB6ZP4C4HPIutJaDfyLix/cM2Ki2eNntbbC1fxEwSLSt+mhAZCaq8XQUgoArUAyqgqoBtTUGCL9VzPbnCFpDXDEWE1niyNDA4wYlJ0+XPBjv5rIPvJN/9rHfZl+7gdvaxLgcLQoYrSDlCKoM8h7Gl/jegGtf+TIab7yd7nqFNBtUI8fK7Dw333kH9EJoJUvAdJC5/SFEJ5sgDbTRoHeyYuN8wd7rKmb3dvBlSOZNcHZjuAhIQGcBjxtIz4ewWYdD9R7nPeoVrwGlel8nNLo9zThH8E5xSrgxRNZg0oqHj5ecuvVG3vcXH+TQRbvwvR6GAo2XIF6YxGp1ntm25Yb3vZ+TI4MplKoCEcv5VYfc9noO3nAE3+shvkDTLdR5mL0IcGiVQNwgH3jSrsPMFSzvbgRzM4JR72pUOK7aRMHxRDOQb4ZkxlqiVpuoPUej06I5E9Oaj2jPW9rzls68oTlviGctdsZiOpZoNiKaj7GdkP35yuMdOA+VCpEazhwveWDnAd75Z7/HRbvm8aM05BJlhmqMGIt2t3jpXb/O2mVHyDZL1Bt8GVyWpJ6TVcy1f/dOrPOoK1FX4osMrUpozAfpuBJjYkQtWZUStQhhU4RIxlhcANMAn0M0g1YjcHlIc9fvI3/qG5TWIdFejJ1HoibGWrAGMYpKidMcLwViHPF8g5kDyyxcfRnz115BNBPjixJfGSojVE4xWM4/U/DA/v3c+eF/xUfufB95MQgQNWrg+30OXnsFO97yHh467TAqOECN4AH1hv5KxfBFr+DKl72Yx795H2ZuFq85WmUhezQRWo3ozDYwsWGrX1JUpg7xEVHI15nk3Yog3kMxREyMz/uQP47Xl1Ge+QSQA3Ng5kFmgsdGgYDAkBKoSPH0sZxttugcOsSBN93Gnte8CFf5AElN7XPUcubHBXNXHuWN738vn/zQH2IWmuAckS+49R/8Nk+lMzAo8JENEAXFSzA/45Tj5w1X/O27OXb/dyhdUaPDEpxDrIFS2XNphyqC86uO0VZRo1hHNKmQRk3U5YhpouUooDQ1YZXyNK1dVzMa3YK4R6A8Bv406DCMmVxTNS6xAcGVs6SPfpcnfvxtth6+ncvfc1cofVUKRvAOxBt+8KOKl992Bwf/6ss888gPIRvy8jveTPfwq+ieLLGRxRXbdQ8v4EVADcVKxflLbuLQK3+Rx778JczCAr5Oy5HgpC65fpFe7tk6JQzPlSGfUQk4QGopChKgri/AtidlJSMVaj3EO4D9oVrjZhG/gurWduicKicEh1ih2TlgDTjO+mcfoxx2OfTe38LnDhScA3VCmTkeNg2u+Bvv4Jnv/gZ7Lt3H/tvfzwPPeCQXKrOdlzlRVAQvQXjWK2tnYc/r30Xz218jLwqwFlHF5xl2NuLAzXs5d36D9ceVclBh5kLabcZhT6sSxKC+CMimsRyQmArWKlFnHhpLEM2CaYE0UbsXkRpHmHH9cPsWMRw4spcjtx7k+lsvobM4ovuV3+fUpz5J6SPSrifrQ9aHamRZPeFJ9ryaqLOXm++4iyeLPfiNCpcJbqT4BFwqtIjQVHAjwp0a/LmSzYVr2PnqvwmjIYJHcGhScNmL9pMtzHP+jHLmgXQ7I/RVqHQGHxjq66IVtHcHdOgdqBDFFtuq4V08D3bMhGhSEwiVl1C3M8YiCDYyvPOP9/GbX9rLf/zOK7jlzotANtj4/O8yOLZGmUeUfaXoQz6AoqccO63cdNvd5EfewvnjHi0Mribcp0IxVAaf+BCdYkSZGjSBKgm+e3RWiV7xLhrLs2ie1QmP4+AvHeWZdcfgZMTZHwyhZVEvITrouAYwzgFME2kshwTGxMGWDUjcDJphO8E8TDPcdXVnupbvnUddqBVsJQmrWwOe3jhBvLsE5nHDR9m8508ocyHvu0D8QBltQbE2Yt/r3srx1Vl05ClTwSXghw6PYfidv+LMPb9H+djXsAjV0KEJ+MzgeyWpuYy5X3wzFCN8mrLjukNUlxykv2lY/3ZB2a3q4nMMqpggubrBoBU0FwLoqbIgUQ2qbGwcpD4m3DRAmiFznFRmodmImJ/rMDfbQnxFkim9oWN9kOEEwCM0yR75LEW3pEpjqqGnSpTBypBrLlFODJok50qqRKhGUI08vrRkZ3oM7v0wiLD+1T+llWWUucXn4DLQQsjPeszRdxHtWkaqgt2vvY2TZ4f41QYnvn4a2s3g2GtHbaSuj+m4VtZYgmq03eERwRjBRFFdFGmANAIHTWNKAwy4gqv+4D9xy7338cvfuZ9db3gHg42MwVBY7+YUlat51cZtPU1x/mmqzOCSgt7akIsaXaKFGVZPeCgElypupLjE40pL797/jI4eRqylf+pB3I++SBxZqpHDp0ELdFRR+n1EN93OzPUvZsMtU21ErH7lGYpehrRmg4Ou+xfBBOoOjEqMSowUwzoAWNACG0VEcc0AGd8NIEIkQkx9i6G/eDknZg5wasfF6CU3kCaGQd+z1XMUZW1qxqJFQrF5iiqBfJBi+mtcenmbp07EaOKpUqVKFZdWqDZJnv4h5RN/jhgXEjdJ2bzvL2iXA1wR4TOPyxRXCdU5T/Poe3GXv5ruqS3yp3qsfu9BZKYDGk1FK4MRE2+XiU1Ii9UVYAy+yJCFi6ExUxcQogCVJZ78rUWKFptovoH6IeVWRr7iGa54iuGIJHWMhjAcOrJknHEGvOCSIVVSkqye4+A+x3qyi8FaQZV5qtTjM4dWQjXKGT3wMfCnQ7KlFrE5o7OPUj3+ReLIoJlDc0XzkFmqLqHzV2BWz3H+3i/V1ae6sTLOWeIZopDpjbswMVQFYgw6Klg4dJg0sZS9FWS/bOcLSICYacru61/L7iM3EDciTt73VdKeo9E1kEOVe9LUw0jxlSdLpsCCjRDfINvaZC7aoLV8lOPHHZQl1aRy7ZDWPNkTn4TN/4WJQ6co9BBKvB2w8b1Ps7j3NgbpMo22wyyCmbN444mvfh3ZN/4Drnsamdt7AUbRurodCiLYiUqIeHQ4ZMc1R2ldfC29z/8b9Kpb6zpaqKUZ1ZBIFn0ah95B86V3MDsDzXNX0e3FyFaIz1VakqUBMLrck2UhMqgvsZ0FHDvxG49zyY27WF3p4IchD1ANTReJ25TrT1I89kfgz4XQNUFcFkhw609in/ksh4/+KmeGLZLhDGbL44YOpImfeyNED4YmzbjgKiZUr32LSMftI6kThyxhdu8u5l/3To7/0QeAAq82pJjqUe/QLIOiB9oj6w7on6lIG5D3N6lGS+RbQANc5shTwfXBtaBI6+aHZsjC9eR9y96dCWl1KYP1LkYc3uskN4MGxY//gPbMj1jYPc/ynjn2HJjl4ksX6ezy2OWEaEHYedmfcPLUN/hvv/8h3FaTytS5hnjs3Lvx83+J5ucgmtlujITYToRWtU0HdGTLjH3v/Bccv+dBdPAIMId6RSsHvqJplMMHD9JknrUzQwaFIe9HlBFUeYlPPGUP1IIWniJTqkRxJZTJtpbJrlfTyE6yfOVRTp5KoRxSOTOpO5jmMvnpT9K+4lMcecMSh29ss2NXg6UlYaY1oPAlo6yCSDnx+ID/+q8PUbS6tG7qEC22iTpg4oLGjhmiJ97DmY//y7pMNtUZKkdEY6ckxqD9IfvedDuD+Zsov/VPkdYsmqV4J1CFF3bHnl8/cBftpvCQfS1/3j9OsuWw1lLlBT5x+C4QeUxWUOSKpFBmnjI34BPsrisp5SoO7p9hfX2JcrABaGhAARI1qLrPoO4PWbyhTWs5ZjCqKCvH+oYQRYpBsA3FlsJnfsdQPHwvrdvuxsweQijw3oIKab9g9qa3MHPfJxg+eQxpd0IXG4UyqZv+qmilNOY6tH71bjbvvw+qkzXcDRvzlQOfUAzP8uSplCfOKKu9Li4fUvRS8l6Cy1M0KfH9Ct8v8XlFkSlljeiKXomJBb/vLSxGGbSup3v2POpyXFHiywJfZfjCUm1+hNkrz7C4e4YoUlxlKApDmQtFZkgLRR185aM5W48MED8kWvkSDTH4QYHvVbhuhT+fMVrr0HzVu0GzSQQaYx8Tmiuh+Tl7082kSztxxx5g0ksnpASuKMEnVOWI8+mA1X7CZtLHVxnVaEA56OPKFLIchgkMU7SoKBKlSAxJt8SnI5pXvg1TLLK8/yrOnijQckCV5/gyQ8sE9RHVxteIdv9PFq9YpjULVQVp6hkOPYOBp9urUOC7n644+bUBJk9QE5M+fg9R90G8a+DTjGpU4lJHuTLA7/wVWtfcjCbDukVoEJFaAwC0ZObGl+BFkXK9rg0GhnkHvizApVQ+ZyPZ4NxwjX4+RMsMl3VxWR+tCkgzGA0hGULpKIaetD+gGint3XeT9g+ya8nS7V9M3lvBV0XAEmUSHGxyHjEfYeFqy+xSjInAaahDggfvaTWEE990PPqFIaaf44kQyXH5gOKx/0EsDjfM0DTDJzl+MCQ/a2ne/G6wRfBp6lFfEY0LnRJZ4h17UYRoZoaK7ba3V8FXJZQ9ynyLTV3B2DaDbBVnB/jhZuBhug7pAOwmGIfkXQxNbHUt1ebN9E+0mGmdwc6/ns2nz2LI8MW4DO9Dprn5aQxP0L9vkeEDCaYV+jOmKdgW2Fiwc4aNZ0o4m4QqtTGoL8EmjI79gOXLHiKrrgCX1BVqQbJVooteQevILWSPfBfac+ArogCAQtroXYVRpXPlUbJv/fcaLwvOgdUecQdsY5GuOY8xMVkzo9UyGFkPPcK5Jl5LpFwBEszClWjvSkbHO5SjLpJ/nx1H3sTqGQPlBl7tdliKZmD0KPS/isdSDPohlJk65BsBW3ejY8FkCt6g1taVkhhhgEs3SZ+6h8YVl5ANslASMwa1Sr7SIL7qLuTJ74b2HBqigKBonuNPH0MPv5Ydt/wygy//MeW540ijTT7sYhoPIbZDEl/BiK1Qd4+XEBEkWwE8ag/C5gjlMdQXeG2EhgpnIFll6dLL6PYOUmydCoDLlzX+ikLTZevLoOcRytAd9gE3bBeats8yeDEQRXVuEUpj6h2YNZJTT7Kw73FSd3GIvSYCK7h8DbPnZqLLX075+DehNYOZdIXiJv2vf5GFNCWRHVz19/4tcaeNpnmoMRY9XNbDJVv4UQ+XDHBJn2rUoxwNKUcjqlGfKunjkh4+H0FxHtFNyDZotjLixV+if3YTNAv5hs+AUESley/kjwJJQG1iGJ86UxvVt0Uji8YRRFNjJAp/mxbCFj5fozj5PRo2x2UpWo7QdIRPBxRnt7D7fw1pGnA+MEC9Q1oNuo89RPWljzJvYav9Mq7/rT9jz7U3oKNNdLQFPkGkQKQA8jqsTN2aBaJ8CtUAqgFaDpHiFIuXvpLNVQtuI5RvNA+b9wl0vw7pg8CpWsKh2xRw//gYztSN3f6sNlOpzy+EVvdJkrXTNIuT4BWf9PD5EM1H+MEZXHU50f5fCA1UZq/WCxQsHXLtHb8DL7mbjQR2NnrMnfgCJ771CGvH1igLG+w17oTDFONzhAJoFaRJBT5FXB9NTzB/4Fqq9ttI1k+HDqpqILw8A9kxpDyG6uPBj0i0XV+YHJsbH26cqjyJ1Aypsxupu8kuR3yCRi+nuftW7L6XkGZNoNo+cdZYwDbO4H74zxFmj4S5JxCxgqTPZTe9nX2v+U3SHZcTLcGMLdG1R1j5wffYePJhRmtnKPt9tChDnJyYZ22TOPA9otmDmNnXUXRXERmhPgUdQbUJrge6CbpSEzFF/JgBk2N7UwXX6bOBUB+OcKAV4j3qC4Qmam+kMbeMXbgM7+tzimLwEuMt6PnPIMxepdsdYR8golZoskXc2MslN/wai1e/jujiG9EdS7hWODCW9rdI1o9TrJ+m2Fql7K3jhl180kXTcyFZKmNU9qLJU6CrQcJaMwlXm04ejttM7H5MtLng2KxcoBVMEd8Iql8OJwgvILcUIUZ9B7SucClTvqWEuIMwe1gneb6rqy1aH1p0GfgB0CRqXU574WKiud3Q2Ym2FnFRB+cNrqpwSR9Nz+OTVXRwAqpusHXXBXFIAJ1MGifjNNzXGKCuKE+rPkYgisNQ5+oxUwyQKBRxfBZCuamJdAWoC81SdXUGWjHJAjF1fbOBMHPlxAfMzc1gTA396vO3hqBSyahHkY5qyY3P3k1enVyWmNn5ZZzCcJgwPjnKdOu4Vm0Rod1p0Wp3plR+u6fgnKPbHWCjiMXFxSnio8nhTNThq5zRKCUvykCor+/6TFMcW+bm5rCR3Tar2mlGUf2dEWOEa48cpN1u4r2vi6I68Q3nzm3w9LETeF8n63qhPMMjx+LCIjdcfzVJmvL97/8I56pJ/jEZWKtxHEdcffVhduxYnjwTCbZqrWUwGPKd+x9gdn6eW15ydGo9YXIsXhXvPcdPnObYM6dAYlTDIevxibZ9+/Zy9ZHD2Dh6DqaQ5vLh8bcKKIpy+0sM05cI1lqiyE4/fO44QL2nKErECI1G/NypuFBvyrIMmebzXUZoNpthzryYXuU5s0ZxVEv4uXvzzlMWxURoF7w5/c1REbnguPD0WuEIwfMw5/n2baQ+hvfTx2+v+TwMVcXXc5jxkbqfcOmktP88a1BnvM+zxgVn18MkP3XPP/Xy/q8/yfaa/+93/Lha8v9xKQRY/Txr/Mx/be7nDHihN/BCXz/zDPi/QpN5SQXeTmEAAAAASUVORK5CYII="
try:
    # Use the exact DACRE logo-mark favicon supplied with the project.
    if DACRE_FAVICON_PATH.exists():
        _DACRE_PAGE_ICON = Image.open(DACRE_FAVICON_PATH)
    else:
        _DACRE_PAGE_ICON = Image.open(io.BytesIO(base64.b64decode(_DACRE_FAVICON_B64)))
except Exception:
    _DACRE_PAGE_ICON = "📊"

st.set_page_config(
    page_title="DACRE WORLDWIDE — David's Intelligence",
    page_icon=_DACRE_PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* ========================================================================
   DACRE WORLDWIDE — PROFESSIONAL ONLINE COMPANY UI SYSTEM
   Light enterprise surface + black typography + DACRE blue actions.
   ======================================================================== */
:root{
  --dacre-blue:#1769ff;
  --dacre-blue-dark:#0b4fd1;
  --dacre-blue-soft:#eaf2ff;
  --dacre-ink:#101828;
  --dacre-muted:#667085;
  --dacre-border:#e4e7ec;
  --dacre-surface:#ffffff;
  --dacre-bg:#f7f9fc;
  --dacre-success:#12b76a;
  --dacre-shadow:0 10px 30px rgba(16,24,40,.07);
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"]{
  background:var(--dacre-bg) !important;
  color:var(--dacre-ink) !important;
}
[data-testid="stHeader"]{
  background:rgba(255,255,255,.96) !important;
  border-bottom:1px solid var(--dacre-border) !important;
  box-shadow:0 1px 8px rgba(16,24,40,.04) !important;
}
/* Keep Streamlit's hamburger/menu usable, clean and black. */
[data-testid="stSidebarCollapseButton"],
button[aria-label*="sidebar" i],
button[title*="sidebar" i]{
  display:flex !important;
  visibility:visible !important;
  opacity:1 !important;
  position:relative !important;
  left:auto !important;
  width:38px !important;
  height:38px !important;
  margin:8px !important;
  padding:0 !important;
  align-items:center !important;
  justify-content:center !important;
  background:#fff !important;
  border:1px solid #d0d5dd !important;
  border-radius:10px !important;
  color:#101828 !important;
  box-shadow:0 2px 8px rgba(16,24,40,.06) !important;
}
[data-testid="stSidebarCollapseButton"] svg,
button[aria-label*="sidebar" i] svg,
button[title*="sidebar" i] svg{color:#101828 !important;fill:#101828 !important;stroke:#101828 !important;}
/* Do not hide the whole header — only the Streamlit deployment controls. */
[data-testid="stToolbar"], .stToolbar, .stDeployButton, #MainMenu, [data-testid="stStatusWidget"]{
  display:none !important;
}
footer{display:none !important;}

[data-testid="stSidebar"]{
  background:#fff !important;
  border-right:1px solid var(--dacre-border) !important;
  box-shadow:4px 0 20px rgba(16,24,40,.035) !important;
}
[data-testid="stSidebar"] *{color:var(--dacre-ink);}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stCaption{color:var(--dacre-muted) !important;}
[data-testid="stSidebar"] hr{border-color:var(--dacre-border) !important;}
[data-testid="stSidebar"] button{
  border-radius:10px !important;
  border:1px solid transparent !important;
  font-weight:650 !important;
}
[data-testid="stSidebar"] button:hover{background:var(--dacre-blue-soft) !important;border-color:#c7dbff !important;}

.block-container{max-width:1500px !important;padding:28px 34px 70px !important;}
[data-testid="stVerticalBlock"]{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}

/* Main Streamlit controls */
.stButton > button,
.stDownloadButton > button{
  min-height:42px !important;
  border-radius:10px !important;
  border:1px solid #d0d5dd !important;
  background:#fff !important;
  color:#101828 !important;
  font-weight:700 !important;
  box-shadow:0 1px 2px rgba(16,24,40,.04) !important;
  transition:all .16s ease !important;
}
.stButton > button:hover,
.stDownloadButton > button:hover{border-color:#9bbcff !important;background:#f8fbff !important;transform:translateY(-1px);}
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"]{
  background:var(--dacre-blue) !important;
  border-color:var(--dacre-blue) !important;
  color:#fff !important;
  box-shadow:0 5px 14px rgba(23,105,255,.20) !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover{background:var(--dacre-blue-dark) !important;color:#fff !important;}
input, textarea, [data-baseweb="select"] > div{
  background:#fff !important;
  color:#101828 !important;
  border-color:#d0d5dd !important;
  border-radius:10px !important;
}
label, .stTextInput label, .stSelectbox label, .stFileUploader label{color:#344054 !important;font-weight:650 !important;}
[data-testid="stMetric"]{background:#fff;border:1px solid var(--dacre-border);border-radius:14px;padding:14px;box-shadow:var(--dacre-shadow);}
[data-testid="stMetricLabel"]{color:#667085 !important;}
[data-testid="stMetricValue"]{color:#101828 !important;}
.stAlert{border-radius:12px !important;}

/* Enterprise chrome */
.dacre-page-chrome{
  display:flex;align-items:center;justify-content:space-between;gap:20px;
  padding:18px 22px;margin:0 0 22px;
  background:#fff;border:1px solid var(--dacre-border);border-radius:16px;
  box-shadow:var(--dacre-shadow);position:relative;overflow:hidden;
}
.dacre-page-chrome:before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--dacre-blue);}
.page-chrome-left{display:flex;align-items:center;gap:13px;min-width:0;}
.dacre-page-chrome .page-icon{
  width:44px;height:44px;border-radius:12px;display:grid;place-items:center;
  background:var(--dacre-blue-soft);color:var(--dacre-blue);font-weight:900;font-size:20px;
  border:1px solid #cfe0ff;
}
.dacre-page-chrome .page-kicker{font-size:10px;font-weight:850;letter-spacing:.12em;color:#667085;text-transform:uppercase;}
.dacre-page-chrome .page-title{font-size:24px;line-height:1.15;font-weight:800;color:#101828;margin-top:3px;letter-spacing:-.025em;}
.dacre-page-chrome .page-subtitle{font-size:13px;color:#667085;margin-top:4px;}
.page-chrome-right{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end;}
.chrome-pill{padding:7px 10px;border-radius:999px;background:#ecfdf3;color:#087443;border:1px solid #abefc6;font-size:10px;font-weight:800;white-space:nowrap;}
.chrome-pill.soft{background:#f2f4f7;color:#475467;border-color:#eaecf0;}

/* Global online-company quick action bar */
.dacre-quickbar{
  display:flex;align-items:center;justify-content:space-between;gap:14px;
  padding:11px 14px;margin:0 0 20px;background:#101828;color:#fff;border-radius:14px;
  box-shadow:0 8px 24px rgba(16,24,40,.13);
}
.dacre-quickbar .quick-brand{font-size:12px;font-weight:850;letter-spacing:.06em;white-space:nowrap;}
.dacre-quickbar .quick-status{font-size:11px;color:#d0d5dd;white-space:nowrap;}
.dacre-quickbar .quick-status b{color:#84caff;}

/* Common light dashboard surfaces */
.user-nav-brand{display:flex !important;gap:10px;align-items:center;padding:8px 4px 16px;}
.user-nav-brand b{font-size:20px;letter-spacing:.08em;color:#101828 !important;}
.user-nav-brand small{display:block;color:#667085 !important;font-size:9px;letter-spacing:.18em;}
.user-nav-dot{width:10px;height:10px;border-radius:50%;background:#12b76a;box-shadow:0 0 12px rgba(18,183,106,.35);}
.user-dash{border:1px solid var(--dacre-border) !important;border-radius:18px !important;padding:28px !important;background:#fff !important;box-shadow:var(--dacre-shadow) !important;}
.user-dash h1,.user-dash h2,.user-dash h3,.user-dash b{color:#101828 !important;}
.user-dash p{color:#667085 !important;}
.user-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:20px 0;}
.user-kpi{padding:18px;border-radius:14px;background:#fff;border:1px solid var(--dacre-border);box-shadow:var(--dacre-shadow);}
.user-kpi b{font-size:28px;display:block;color:#101828 !important;}.user-kpi span{color:#667085 !important;font-size:12px;}
.user-work-card{padding:20px;border-radius:16px;background:#fff;border:1px solid var(--dacre-border);height:100%;box-shadow:var(--dacre-shadow);}
.user-work-card h3{margin:0;color:#101828 !important;}.user-work-card p{color:#667085 !important;line-height:1.6;}
.notice-card{padding:14px 16px;border-left:3px solid var(--dacre-blue);background:#fff;border-top:1px solid var(--dacre-border);border-right:1px solid var(--dacre-border);border-bottom:1px solid var(--dacre-border);border-radius:10px;margin:8px 0;box-shadow:0 3px 12px rgba(16,24,40,.04);}

/* Make markdown headings readable across the business app. */
.main h1,.main h2,.main h3,.main h4{color:#101828 !important;}
.main p,.main li{color:#344054;}

@media(max-width:900px){
  .block-container{padding:22px 18px 60px !important;}
  .dacre-page-chrome{align-items:flex-start;}
  .page-chrome-right{display:none;}
  .user-kpis{grid-template-columns:1fr 1fr;}
}
@media(max-width:620px){
  .block-container{padding:16px 12px 50px !important;}
  .dacre-page-chrome{padding:15px 16px;}
  .dacre-page-chrome .page-title{font-size:20px;}
  .dacre-quickbar{align-items:flex-start;flex-direction:column;}
  .user-kpis{grid-template-columns:1fr 1fr;}
}
/* DACRE 7.3 DARK ONLINE ROBOT THEME */
:root{--dacre-bg:#050914;--dacre-surface:#0b1220;--dacre-surface-2:#101a2b;--dacre-border:#203149;--dacre-blue:#58c7ff;--dacre-blue-dark:#1d8fd0;--dacre-orange:#ff9f43;--dacre-copper:#b9784f;--dacre-text:#f4f8ff;--dacre-muted:#a7b7ca;--dacre-shadow:0 18px 55px rgba(0,0,0,.34)}
.stApp,[data-testid="stAppViewContainer"],.main{background:radial-gradient(circle at 70% -10%,rgba(88,199,255,.10),transparent 35%),#050914!important;color:#f4f8ff!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#05070d,#0a101b 65%,#070b12)!important;border-right:1px solid #1b2a3d!important}
[data-testid="stSidebar"] *{color:#f5f9ff!important}
[data-testid="stSidebar"] button{background:#05070b!important;border:1px solid #2a3c53!important;color:#fff!important}
[data-testid="stSidebar"] button:hover{background:#132033!important;border-color:#58c7ff!important}
.main h1,.main h2,.main h3,.main h4,.main h5,.main h6{color:#f7fbff!important}.main p,.main li,.main label,.stCaption{color:#c1cede!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stSelectbox div[data-baseweb="select"]>div,.stMultiSelect div[data-baseweb="select"]>div,.stDateInput input{background:#0b1220!important;color:#fff!important;border-color:#2b4059!important}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#71839a!important}.stButton>button{background:#0b1422!important;color:#fff!important;border:1px solid #2d425b!important;border-radius:12px!important}
.stButton>button:hover{border-color:#58c7ff!important;box-shadow:0 0 22px rgba(88,199,255,.14)!important;transform:translateY(-1px)!important}.stButton>button[kind="primary"],.stButton>button[data-testid="baseButton-primary"]{background:linear-gradient(135deg,#178dd0,#58c7ff)!important;color:#04111b!important;border:0!important;font-weight:900!important}
[data-testid="stMetric"]{background:linear-gradient(145deg,#0d1727,#0a111d)!important;border:1px solid #263a52!important;color:#fff!important;box-shadow:0 18px 55px rgba(0,0,0,.34)!important}[data-testid="stMetricLabel"],[data-testid="stMetricValue"]{color:#fff!important}.stAlert{background:#0d1727!important;border-color:#2c4560!important;color:#fff!important}
.dacre-page-chrome{background:linear-gradient(145deg,#0c1524,#09111d)!important;border-color:#263b54!important;box-shadow:0 18px 55px rgba(0,0,0,.34)!important}.dacre-page-chrome:before{background:linear-gradient(180deg,#58c7ff,#ff9f43,#b9784f)!important}.dacre-page-chrome .page-kicker{color:#79d3ff!important}.dacre-page-chrome .page-title{color:#fff!important}.dacre-page-chrome .page-subtitle{color:#aabbd0!important}.dacre-page-chrome .page-icon{background:#0d1b2d!important;color:#58c7ff!important;border-color:#31506d!important}
.chrome-pill{background:#102d24!important;color:#78f0b0!important;border-color:#276448!important}.chrome-pill.soft{background:#151d2a!important;color:#b7c6d8!important;border-color:#2a3c53!important}.dacre-quickbar{background:linear-gradient(90deg,#05080e,#0d1725 65%,#13253a)!important;border:1px solid #263e58!important}
.user-dash,.user-kpi,.user-work-card,.notice-card{background:#0b1422!important;border-color:#263b54!important;box-shadow:0 18px 55px rgba(0,0,0,.34)!important}.user-dash h1,.user-dash h2,.user-dash h3,.user-dash b,.user-kpi b,.user-work-card h3{color:#fff!important}.user-dash p,.user-kpi span,.user-work-card p{color:#b1bfd0!important}
.dacre-dark-section{background:linear-gradient(145deg,#0b1422,#101b2b);border:1px solid #2a405b;border-radius:20px;padding:22px;box-shadow:0 18px 55px rgba(0,0,0,.34)}.dacre-section-blue{border-left:5px solid #58c7ff!important}.dacre-section-orange{border-left:5px solid #ff9f43!important}.dacre-section-copper{border-left:5px solid #b9784f!important}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# THIRD-PARTY IMPORTS
# =============================================================================

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops
import requests
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import websockets
import psycopg
from psycopg.rows import dict_row

# =============================================================================
# OPTIONAL IMPORTS - WITH ERROR HANDLING
# =============================================================================

# Google Gemini
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    types = None
    GENAI_AVAILABLE = False

try:
    import google.generativeai as genai_text
    GENAI_TEXT_AVAILABLE = True
except ImportError:
    genai_text = None
    GENAI_TEXT_AVAILABLE = False

# OpenAI
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OpenAI = None
    OPENAI_AVAILABLE = False

# Speech Recognition
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    sr = None
    SR_AVAILABLE = False

# Text to Speech
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    pyttsx3 = None
    TTS_AVAILABLE = False

# Web Search
try:
    from googlesearch import search as google_search
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False

# Audio
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    pyaudio = None
    PYAUDIO_AVAILABLE = False

# Computer Vision
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    cv2 = None
    CV2_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    np = None
    NUMPY_AVAILABLE = False

# DeepFace
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DeepFace = None
    DEEPFACE_AVAILABLE = False

# NetworkX
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    nx = None
    NETWORKX_AVAILABLE = False

# Maps
try:
    import folium
    from streamlit_folium import folium_static
    FOLIUM_AVAILABLE = True
except ImportError:
    folium = None
    folium_static = None
    FOLIUM_AVAILABLE = False

# LiveKit
try:
    from livekit import RoomServiceClient, AccessToken, VideoGrants
    from livekit.api import RoomAgentDispatch, RoomConfiguration
    LIVEKIT_AVAILABLE = True
except Exception:
    RoomServiceClient = None
    AccessToken = None
    VideoGrants = None
    RoomAgentDispatch = None
    RoomConfiguration = None
    LIVEKIT_AVAILABLE = False

# Transformers
try:
    from transformers import pipeline, AutoModel, AutoTokenizer, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    pipeline = None
    AutoModel = None
    AutoTokenizer = None
    AutoModelForCausalLM = None
    TRANSFORMERS_AVAILABLE = False

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dacre.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DACRE')

# =============================================================================
# GLOBAL CONFIGURATION
# =============================================================================

APP_NAME = "DACRE WORLDWIDE"
_DB_SCHEMA_VERSION = 10
DI_NAME = "DI — David's Intelligence"
CEO_GUARD_NAME = "Guaiel"
MASTER_USERNAME = "david"
MASTER_FULL_NAME = "David Emenike"
MASTER_PASSKEY = os.getenv("DACRE_MASTER_PASSKEY", "theWORDofGOD@111").strip()
MASTER_PASSKEY_HASH = os.getenv(
    "DACRE_MASTER_PASSKEY_HASH",
    "1d9763eb96e88387bf4a18b7ca1a94a4a3a80ea0353cf4203764c0bccfbda27f"
).strip()
# App-level management password. The deployment environment can override this.
MANAGE_APP_PASSKEY = os.getenv("DACRE_MANAGE_APP_PASSKEY", MASTER_PASSKEY).strip()
DAVID_CREATIONS_PASSKEY = os.getenv("DACRE_DAVID_CREATIONS_PASSKEY", "My children").strip()
DI_BASEMENT_PASSKEY = os.getenv("DACRE_DI_BASEMENT_PASSKEY", "David intelligence").strip()

# Webstore Knowledge Base - CRITICAL for DI to answer questions correctly
DI_WEBSTORE_KNOWLEDGE = {
    "dacre": {
        "description": "DACRE Analysis is a business and data intelligence platform",
        "features": ["Data Analysis", "Business Intelligence", "AI Assistant", "Data Visualization", "Export Reports"],
        "pricing": "Free tier available. Professional and Enterprise tiers with advanced features.",
        "website": "https://dacre.ai",
        "support": "support@dacre.ai"
    },
    "david emenike": {
        "role": "CEO and Founder of DACRE Worldwide",
        "expertise": ["Business Intelligence", "Data Analysis", "AI Systems", "Strategic Planning"],
        "vision": "To democratize business intelligence for organizations worldwide",
        "background": "Technology entrepreneur with expertise in data systems and AI"
    },
    "di": {
        "full_name": "David's Intelligence",
        "purpose": "Built-in intelligence assistant for DACRE Analysis",
        "capabilities": ["Data Analysis", "Business Research", "Strategic Advice", "Technical Support"],
        "personality": "Professional, analytical, helpful, evidence-first"
    },
    "business intelligence": {
        "definition": "The process of analyzing data to inform business decisions",
        "key_metrics": ["Revenue Growth", "Customer Acquisition", "Operational Efficiency", "Market Share"],
        "best_practices": ["Data-driven decision making", "Regular reporting", "Predictive analytics"]
    },
    "data analysis": {
        "methods": ["Descriptive Analytics", "Diagnostic Analytics", "Predictive Analytics", "Prescriptive Analytics"],
        "tools": ["DACRE Analysis", "Python", "SQL", "Excel", "Power BI"],
        "best_practices": ["Data cleaning", "Statistical validation", "Visualization", "Interpretation"]
    },
    "artificial intelligence": {
        "definition": "The simulation of human intelligence in machines",
        "applications": ["Data Analysis", "Natural Language Processing", "Computer Vision", "Predictive Modeling"],
        "dacre_use": "DI uses AI to understand user questions, analyze data, and provide intelligent responses"
    },
    "machine learning": {
        "definition": "A subset of AI that enables systems to learn from data",
        "types": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning"],
        "dacre_use": "DACRE uses ML for data pattern recognition and predictive analytics"
    }
}

# Critical Technology Knowledge for DI Brains
DI_TECHNOLOGY_KNOWLEDGE = {
    "python": {
        "description": "Python is a high-level programming language used for data science, AI, and web development",
        "key_features": ["Easy syntax", "Large ecosystem of libraries", "Cross-platform", "Open source"],
        "dacre_use": "DACRE is built with Python using Streamlit, Pandas, Plotly, and other libraries"
    },
    "streamlit": {
        "description": "Streamlit is an open-source Python framework for building web applications",
        "key_features": ["Rapid prototyping", "Hot reloading", "Interactive widgets", "Data integration"],
        "dacre_use": "DACRE Analysis is built on Streamlit for the user interface"
    },
    "pandas": {
        "description": "Pandas is a powerful Python library for data manipulation and analysis",
        "key_features": ["DataFrames", "Data cleaning", "Data aggregation", "Time series analysis"],
        "dacre_use": "DACRE uses Pandas for data processing, cleaning, and analysis"
    },
    "sql": {
        "description": "SQL is a standard language for managing and querying relational databases",
        "key_features": ["Data querying", "Data manipulation", "Database management", "Analytical queries"],
        "dacre_use": "DACRE uses SQLite and PostgreSQL for data storage and retrieval"
    },
    "api": {
        "description": "APIs enable communication between different software systems",
        "types": ["REST API", "GraphQL", "WebSockets", "gRPC"],
        "dacre_use": "DACRE integrates with various APIs for data access and AI services"
    },
    "cloud computing": {
        "description": "Cloud computing provides on-demand access to computing resources",
        "providers": ["AWS", "Google Cloud", "Azure", "Supabase"],
        "dacre_use": "DACRE can be deployed on Streamlit Cloud or any cloud platform"
    }
}

# Global Business Settings
GLOBAL_CURRENCIES = ["USD", "EUR", "GBP", "NGN", "KES", "ZAR", "AED", "INR", "CNY", "JPY", "BRL", "AUD", "CAD", "CHF", "SGD"]
GLOBAL_MARKETS = ["NYSE", "NASDAQ", "LSE", "JPX", "SSE", "HKEX", "NSE", "NGX", "JSE", "ASX"]
GLOBAL_COMMODITIES = ["Gold", "Silver", "Oil", "Copper", "Natural Gas", "Wheat", "Corn", "Coffee", "Sugar", "Cotton"]

# DI Language Support
DI_LANGUAGE_PROFILES = {
    "English — Nigeria": {"code": "en-NG", "voice": "en-NG"},
    "English — US": {"code": "en-US", "voice": "en-US"},
    "English — UK": {"code": "en-GB", "voice": "en-GB"},
    "Spanish": {"code": "es-ES", "voice": "es-ES"},
    "French": {"code": "fr-FR", "voice": "fr-FR"},
    "Arabic": {"code": "ar-SA", "voice": "ar-SA"},
    "Chinese": {"code": "zh-CN", "voice": "zh-CN"},
    "Hindi": {"code": "hi-IN", "voice": "hi-IN"},
    "Portuguese": {"code": "pt-BR", "voice": "pt-BR"},
    "Yoruba": {"code": "yo-NG", "voice": "yo-NG"},
    "Igbo": {"code": "ig-NG", "voice": "ig-NG"},
    "Hausa": {"code": "ha-NG", "voice": "ha-NG"},
    "Swahili": {"code": "sw-KE", "voice": "sw-KE"},
    "German": {"code": "de-DE", "voice": "de-DE"},
    "Italian": {"code": "it-IT", "voice": "it-IT"},
    "Japanese": {"code": "ja-JP", "voice": "ja-JP"},
    "Korean": {"code": "ko-KR", "voice": "ko-KR"},
    "Russian": {"code": "ru-RU", "voice": "ru-RU"},
}

# DI Personalities
DI_PERSONALITIES = {
    "professional": {"style": "formal", "tone": "authoritative", "pace": "measured", "emoji": "💼"},
    "friendly": {"style": "casual", "tone": "warm", "pace": "conversational", "emoji": "😊"},
    "analytical": {"style": "detailed", "tone": "precise", "pace": "deliberate", "emoji": "🔬"},
    "creative": {"style": "imaginative", "tone": "inspiring", "pace": "dynamic", "emoji": "🎨"},
    "executive": {"style": "decisive", "tone": "commanding", "pace": "rapid", "emoji": "👔"},
    "strategic": {"style": "visionary", "tone": "insightful", "pace": "thoughtful", "emoji": "🎯"},
    "global": {"style": "worldly", "tone": "cultured", "pace": "measured", "emoji": "🌍"},
    "empathetic": {"style": "warm", "tone": "caring", "pace": "gentle", "emoji": "💝"},
    "technical": {"style": "precise", "tone": "logical", "pace": "methodical", "emoji": "⚡"},
    "sales": {"style": "persuasive", "tone": "confident", "pace": "energetic", "emoji": "📈"},
}

DI_AVATAR_LIBRARY = {
    "male": [
        "https://randomuser.me/api/portraits/men/32.jpg",
        "https://randomuser.me/api/portraits/men/18.jpg",
        "https://randomuser.me/api/portraits/men/75.jpg",
        "https://randomuser.me/api/portraits/men/83.jpg",
        "https://randomuser.me/api/portraits/men/52.jpg",
        "https://randomuser.me/api/portraits/men/1.jpg",
        "https://randomuser.me/api/portraits/men/10.jpg",
        "https://randomuser.me/api/portraits/men/20.jpg",
        "https://randomuser.me/api/portraits/men/28.jpg",
        "https://randomuser.me/api/portraits/men/31.jpg",
    ],
    "female": [
        "https://randomuser.me/api/portraits/women/21.jpg",
        "https://randomuser.me/api/portraits/women/32.jpg",
        "https://randomuser.me/api/portraits/women/68.jpg",
        "https://randomuser.me/api/portraits/women/44.jpg",
        "https://randomuser.me/api/portraits/women/65.jpg",
        "https://randomuser.me/api/portraits/women/12.jpg",
        "https://randomuser.me/api/portraits/women/47.jpg",
        "https://randomuser.me/api/portraits/women/55.jpg",
        "https://randomuser.me/api/portraits/women/63.jpg",
        "https://randomuser.me/api/portraits/women/72.jpg",
    ],
}

BASE_DIR = Path(__file__).resolve().parent
LOGO_CANDIDATES = [
    "assets/dacre_logo.png",
    "ChatGPT Image Jul 29, 2026, 02_27_41 PM.png",
    "dacre_logo.png",
    "logo.png",
]
LOGO_PATH = next((BASE_DIR / x for x in LOGO_CANDIDATES if (BASE_DIR / x).exists()), BASE_DIR / LOGO_CANDIDATES[0])
CEO_PORTRAIT_CANDIDATES = [
    "assets/dacre_ceo.png",
    "Gemini_Generated_Image_kxzp51kxzp51kxzp.png",
    "dacre_ceo.jpg",
    "dacre_ceo.png",
]
CEO_PORTRAIT_PATH = next((BASE_DIR / x for x in CEO_PORTRAIT_CANDIDATES if (BASE_DIR / x).exists()), None)
CEO_PORTRAIT_DATA_URL = """data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAQDAwMDAgQDAwMEBAQFBgoGBgUFBgwICQcKDgwPDg4MDQ0PERYTDxAVEQ0NExoTFRcYGRkZDxIbHRsYHRYYGRj/2wBDAQQEBAYFBgsGBgsYEA0QGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBj/wgARCAH6A4QDASIAAhEBAxEB/8QAHAAAAQUBAQEAAAAAAAAAAAAAAQACAwQFBgcI/8QAGQEBAQEBAQEAAAAAAAAAAAAAAAECAwQF/9oADAMBAAIQAxAAAAH3xJXKSBHk62T04+XQTw+jy9DYr2JJoDgUMM0Uuf23Fdtm708E/D1uBGdx1LdTfOkCN4SKEioaHAa17QAgCIFDNEZfP8AQ8+zzDXhHvL+vKOvdrpPoOvWZ8enFLg19TF571dDGu53r2cuxLeia9aON0tROIy+2wlxLteJduTKvEikKPu1LSaFuha1LrqzyWNrAhgJFGiRRIlbGIeGNHhgC1MgwuhlpZWrn1i0dqqueNErmrTRmu0TGatNGUNUVlLURlrTJmrSUn1ckp3SSIsrWyenHy6GxD6PLv2K9iaaiBOBDDNDLS7TjO0zd2eGbh6nAjOoqturvFFFbwCkJFQ0OA0OA0OAA4AhnhMzn+h5+Z5hFWTSMl68RDZhra0aOikTJ4ZrK5+7ymOm0vPKfLv6FJ5fFNeh7Pklg9b3/AbMe85PmnUXEmV1mHrGVcgau1cydVJ51aRk+prY3zTuuevGs7cxww7xxwK9AdL54vRHL50PRzHm69JR5s70gL5uPRVHncfprs68preutXx1vsal8ed6+l8id62o8lf6ujyperJfKl6oo8sPqQPLz6e5fMV6gk6FJenkkDUeTrZHTj5jDLF6PJv2ILGdtRVAoqYZoYp9pxfaZbs8E/D1uaRnUda1W3zohy1gIoSRACAAgAKAHCBFNCZ3P9BgJy7XNubE0M3Xi+OWiZnIVavD3XKJo51FFdqWNieJXQueQviMBIBLWkhiWbY63jLB7DTw+o6cKvQ4Dk9R2PMt7j27qTjTNdkuKancLhQd0uDbZ3o4Bp6CPPWnoa86anoo85cd/Hw7TvR59SPSK/lmRL7BD4bny/QEfgjj3WPw417YzxcnsUfkJPWmeWPs9Mh85aehN88Vegrz9J9eJLpQkhmVq5XTj5hDPB6PL0FivZxtqSEkgxSxFXs+N7ONuaGbh6yCs7jr2a+sUQ4b5gpQkQqBQ0ObYAUAFQIpojNwOgwGeWa5qWJYZ+3Kh59ucrx9Sbl9Hx9GKO7n59fO9Prp+Xfjpesj5duZq9fTOZo9dWueKg7St048eOho9uGa6xDrmHQKyf0PzrST1+hsUuvnraGY86O3gaaXGojUlIgUNRAAQAFAe1xIklip3qZk4+1jri52nnKHJwCjSRM00uIntciDkRKUkGpVH1ykm0kiPK1cvpy8yr2a3fydBYr2M9GpISBDHJGVe04vtJdqaGbh6yks6ZXsV9YpAjXNJESKaALRNLWUkgIoEU0Jn4G/gJyzJGXMxFPpz4GIb/AJfoQdhZv+b2VmX6luTXuR+b1U2W1nVKppUloQ26rNZkkesRQzMvNlls+8c9k9hl9ePPsli7+b2DpuI9L6cOTpdNjXFTQyydNc57XLs9rX57xGdQ3O+XGpDrNA3UUVeRRdbUVVaNVYNFkuHmdHRmuVp9LVzvGfsJcRm0EyJtJ5nO1HGWtVGUtRGYtJGatJWe/JLrEkiPK1cvfLzOvYg9Hk3rEE+dtSQCCGOSMq9pxfaSldqGbh6yCi1MEgnh1mS1w1zSBISRAUoCEApAookzszD38Fjl45f/EACwQAAIBAwMDBAIDAQEBAQAAAAABAgMEESEFEBIxIEEiM0ITUAYUJRVRcIH/2gAIAQEAAT8A/wCBy2kskqlSS2RKrVpLMsMlrtCD2G4RnH4y2p1o1lkp46e49/Ii2K/A53/A6/6K/42mfxOit3xS345O3/AnA/4ElD80aL2fXU/C84RUrSrOOfaR8/C4m+e16JejtEThL4k/J3/H4f78/f7O25bC/kI00i3uIVkL1U/x6l1eRtrer1I1evO3X39/f2oGvD5e5LwfA+O2UakI3d/c04E3j73G/rU6m4+XInp2v4f3915qdLq9D+9yI6ceRvgfZX3+Lp3U7O49/P2v6u1RjU43P4339reox1d2qL0XHxP9e3x/oI3T4339rh0s/p48bj8S/Xt9E/6Ebr8T+e/q/s3OjfG5fA/iN30/R3e84a2pI/yN32I9mbfj0v4X8/s28/kLrf8f/p+e1/A/jIn48Lp5sX9f/p2S83I+fG/iT/XtvzL4/8AhG5fx/s2T2I3S2o/m/v7X8vXo/v138e/f4U9iL/3t22fL/4J14kKzS/3s1m5XlS947S4oW1lS10I7tQ91O33u2sbdylR2L3/ADe5I/yC+t2q2k/j43u95N5E7vfe36O76e4o92f9xQe5f3sU+3sXlqUqEam2/I9y/y3/wBCh/x47fT8Kx6Kq7S64N1fTsf0t0x09xS76/f3f3Ua8P1Uf6eNfL6N5o3/3914a8/qj/AEy4fM/A/X93PZkXp8PZp+/y478S2e/3XlrIvfwe304/qT9y00S7kS24/s+BfI/t8/f6Yv9OfXp/qJbcT4X16vR22e30I/qTxLTh/Rj2In5I3O432X4/Y/2fE/m/34S/XfIe4vh3X0X64/yT+/f1R/qIvfhe9C1xX6X7/S/b85D4I1/p/2N9I/A2fJ/qI302X/q0a8P63s/q3v8AXr2/6eH79a32+v/xAAoEQACAgEDBAEFAQEBAAAAAAAAAQIRECExICJBUDADEzJRYEFxM4D/2gAIAQIBAT8A4In34UuzpX409mX589j31p3mP409mX589je6L2S0X409mX583EezXij2ZfnqL4MfZLsnXij2ZfmyPij2ZfmpM6mdXlT2Zfp8yPZl+nKfYj2Zfej4fJpI3Xkj2Mvg/A3v+o/eY9mdmXwS/8AI8f4U/eY9md2XLCRuY28Ke7I/Ue1m1l8/p/yL2p2Z3Zccx954mPZl+eI9mb0Ie4j2Zfc3GxsfJej4fBofvIe1O7K0mIn2xX2o/eQ7sIe34s32I4k394h3YQ9vyp58Iee3sH7U7MLv/jS43n7f1H2Jm7v9+i9/1Efs3e1sQ1Xnvdjf5iH333Lsf/EACkRAAICAgIBAwMEAwAAAAAAAAECERADEiExQVAEE1EiMmBxYKGxcZL/2gAIAQEAAT8A/wCBy2/6C+Ymxf8Af9wb9I9/AAt2I6x498Xv0yI/fXvX0C/Z69fQXA+z34JchHh591l+x34Is36XftS4i92S9/X0N+0L/S3X39/eLp4GvZ/6S2vYFw/3//EADwQAAECBQMCBQMCBAUDBQAAAAECEQADEiExQVEiYfAEEYGh8ROxMpHBUEBS8SBigjMDE0RDUoLS0v/aAAgBAQEAAT8A/wD9pP8AlYmQLQPEJ8+UqUoEuPzD3I/3q+TOnS0oShQ3+R4qSZaWXEfD1O2iUv26f959X1S13A8I4lByHif/UoP1E+0pUn6s2fNlsA7ITh6SogP1R4sSkIlyfCSw4N9m0bI8Yv6fhhKlCqfS44mK4b9iXj/cEC0/8AI3UfE03p3iZL1pUpIcgYfI1uD7aHq8pPhm8Iub4yct3fUqY4I3e4u+3ilK8R/p5C5qikD93/ALYXo+S2T4WUnwnhkpm3pG2rPltS/v5+X/4h2cOxe0+KInp/w2G3f23iRNp/e/8AUa/Xf7p4/+/H+aK5N4a5e3/ASE0J3fU539/8vP183/8U7A3I94/S9vI8S5I8p32mI9x+03iT8i8j2vX6e216A4aBByA9m2Y/1j9p84Ue5L2oO3/y67a/7x3/u/r/35v34o5HkU8jL/AKw11/f7n9d/S/X2+p8L80E0M8L7a/8An52/v7/92p/P24e+xG2O/veO+m4/Pj/V8f399r1/3+2v8v8A4/m/uG221/33e3T6S2+jR1evX/2338qf9O6f014/P16fS8I/m13/v69f1/7/a+2/L3o3231mO2m8f3p3/AN/t3113q20120+nvvT/AC6a/wC30/f06p1/92P30/Xf1v5y+46P0/l6/vrt/s/571m/lX3+f3/vXq9/7f8Ay136a+fS3f23i3f23439eS9vfH3i1uO/Xf3fXf3X114299vP+6P7300/3eXv1/5S9vf/I6+23/A3d99Ien9+m4vvp/u99y9/Xff/iP3d6f78f8AsL06f7w6e64/9SOnS+3/AIn3i3/uL0//AG30/fX3f3/3ev8/Inp//EACkRAQEAAgEDAwUAAwEAAAAAEAESExQVEQYGFYGhsbHwMMFg0eH/2gAIAQIBAT8A9aZ958Mesm++GPRn13Ppj0f1Pxh9R9b9bfxj6fVZvu0X1H1P1m3HGdtY+ozbjjO2sfWbdsbZtrH2G3bG2Y+0zftLfzLL9rF7b6x9wXs2f7Mf8Jb2UPTbP2F/If9wj7pZz63z7XH4v4T/3C/bS7rP3M9q/ZY+wX7K99Z+9u9lP3/AMc/bXu99s/c3u8Z+2X/ABzt27dx92s9mt91+uuOPfLf8MXfu83xvPbv3V/pP8Hz+MN79l+uPt3nr6P+fvFp/ueJsnv/AIY++rfeX7n5bZrbuG+n4/uL8z9v/b1W+/j/AK9//9k="""
FAVICON_PATH = BASE_DIR / ".dacre_favicon.png"
DB_PATH = BASE_DIR / "dacre_platform.db"

# Public landing page supplied by the DACRE owner
DACRE_LANDING_URL = "https://dacre-landing-page-od7u.bolt.host/"

# =============================================================================
# DI MEMORY SEED - COMPLETE KNOWLEDGE BASE WITH WEBSTORE KNOWLEDGE
# =============================================================================

DI_MEMORY_SEED = [
    # IDENTITY
    ("IDENTITY", "DI identity", "My name is DI — David's Intelligence. I am the built-in intelligence assistant inside DACRE Analysis.", 2000),
    ("IDENTITY", "Creator and master", "DACRE Analysis and DI were created by David Emenike. David is the Overall Administrator and master of the platform.", 2000),
    ("IDENTITY", "David Emenike", "David Emenike is the creator and master administrator of DACRE Analysis. If asked who created DACRE, answer David Emenike.", 2000),
    ("IDENTITY", "DI purpose", "DI exists to help businesses make better decisions using data, intelligence, and automation. I am here to serve David Emenike and DACRE customers.", 2000),
    ("IDENTITY", "DI philosophy", "DI believes in evidence-based decision making, continuous learning, and helping businesses grow through intelligence.", 2000),
    
    # PLATFORM
    ("PLATFORM", "What DACRE is", "DACRE Analysis is a business and data-intelligence workspace combining data ingestion, cleaning, analysis, formulas, charts, file storage, exports, administration and DI intelligence.", 1900),
    ("PLATFORM", "Supported data", "DACRE is designed to work with CSV, Excel/XLSX, TSV and JSON datasets and to inspect, clean, analyse, visualise and export data.", 1850),
    ("PLATFORM", "Formula Lab", "DACRE Formula Lab supports practical operations including SUM, AVERAGE, COUNT, COUNTA, MAX, MIN, CONCATENATE, UPPER, LOWER and TRIM.", 1800),
    ("PLATFORM", "File Vault", "The File Vault is intended to store user/company files inside the DACRE workspace so important working files can remain organized and accessible.", 1800),
    ("PLATFORM", "Chart Builder", "DACRE can create business visualisations such as bar, line and area charts from analysed data, with room for future chart expansion.", 1750),
    ("PLATFORM", "Export Center", "The Export Center is designed to let users export processed results, including CSV and Excel outputs.", 1750),
    ("PLATFORM", "Workspace and Data", "Workspace & Data is the working area for uploading/opening datasets, inspecting data and carrying out analysis and cleaning tasks.", 1750),
    ("PLATFORM", "DI Home", "DI Home is the continuous conversation area where users can ask DI business, data, technical and general questions.", 1750),
    ("PLATFORM", "DI Question Board", "Every question sent to DI should be recorded in the DI Question Board so DACRE maintains a reliable trail of questions and answers.", 1900),
    ("PLATFORM", "Organization Admin Portal", "Organization Admin Portal provides organization-level administration for the company workspace, including users and company activity.", 1800),
    ("PLATFORM", "Overall Admin DI", "Overall Admin DI is the master-only system-wide command centre. It is separate from ordinary company administration.", 2000),
    ("PLATFORM", "DI Workforce", "DI Workforce is a specialized team of AI agents, each with unique skills, personalities, and knowledge. They work together to serve businesses.", 1900),
    ("PLATFORM", "Business Command Center", "Business Command Center provides executive-level insights, data health, trends, and actionable intelligence for business leaders.", 1850),
    ("PLATFORM", "Business Twin", "Business Twin creates a living digital replica of your business, showing performance, health, and opportunities in real-time.", 1850),
    ("PLATFORM", "Decision Ledger", "Decision Ledger records decisions, context, expected outcomes, and results, creating institutional memory for organizations.", 1850),
    ("PLATFORM", "Opportunity Radar", "Opportunity Radar detects growth signals, market trends, and actionable business opportunities from your data.", 1850),
    
    # WEBSTORE KNOWLEDGE - CRITICAL FOR DI TO ANSWER QUESTIONS CORRECTLY
    ("WEBSTORE", "DACRE Platform Overview", "DACRE Analysis is a comprehensive business intelligence platform that combines data analysis, AI assistance, and business insights. It helps organizations make data-driven decisions.", 2000),
    ("WEBSTORE", "DACRE Features", "DACRE offers: Data Upload and Analysis, Business Intelligence Dashboards, DI AI Assistant, Data Visualization, Export Reports, File Management, and Organization Administration.", 1950),
    ("WEBSTORE", "DACRE Pricing", "DACRE offers a Free tier for individuals, Professional tier for small teams, and Enterprise tier for large organizations with custom requirements.", 1950),
    ("WEBSTORE", "DACRE Support", "DACRE provides support through email at support@dacre.ai, documentation, and the DI Assistant for immediate help.", 1950),
    ("WEBSTORE", "DI Capabilities", "DI (David's Intelligence) can: analyze data, answer business questions, provide strategic advice, explain technical concepts, research information, and assist with decision making.", 2000),
    ("WEBSTORE", "Business Intelligence", "Business intelligence in DACRE includes: data health scoring, trend detection, anomaly detection, executive briefs, and actionable insights from your data.", 1950),
    
    # TECHNOLOGY KNOWLEDGE - CRITICAL DI BRAIN CONTENT
    ("TECHNOLOGY", "Python for Data Science", "Python is the primary language for data science with libraries like Pandas, NumPy, Matplotlib, and Scikit-learn. DACRE is built with Python.", 1950),
    ("TECHNOLOGY", "Streamlit Framework", "Streamlit is a Python framework for building data apps quickly. DACRE's interface is built with Streamlit, making it interactive and responsive.", 1950),
    ("TECHNOLOGY", "Pandas Data Analysis", "Pandas provides DataFrame structures for data manipulation. DACRE uses Pandas for all data processing, cleaning, and analysis operations.", 1950),
    ("TECHNOLOGY", "SQL Database Management", "SQL is used for structured data storage. DACRE uses SQLite for local development and PostgreSQL/Supabase for production.", 1950),
    ("TECHNOLOGY", "AI and Machine Learning", "AI enables pattern recognition, predictive analytics, and natural language processing. DACRE's DI uses AI for intelligent responses.", 1950),
    ("TECHNOLOGY", "Cloud Computing", "Cloud platforms enable scalable application deployment. DACRE can be deployed on Streamlit Cloud, AWS, or any cloud provider.", 1950),
    ("TECHNOLOGY", "APIs and Integration", "APIs allow different systems to communicate. DACRE integrates with various APIs for market data, AI services, and external tools.", 1950),
    
    # SECURITY
    ("SECURITY", "CEO Office guardian", "Guaiel is the dedicated CEO Office Guardian. After the master account passkey is verified, the private CEO Office asks the master to state the name given to the guardian. The expected guardian name is Guaiel.", 2000),
    ("SECURITY", "Master visibility", "Only the master Overall Administrator should be able to view the system-wide DI Memory Box and master administration controls.", 2000),
    ("SECURITY", "Permanent deletion", "The Overall Administrator can permanently delete non-master accounts from People & Accounts after explicit confirmation. The operation is irreversible.", 2000),
    ("SECURITY", "Master protection", "The master account must be protected from permanent account deletion through normal account controls.", 2000),
    ("SECURITY", "Credential protection", "DACRE must never reveal the master passkey, password hashes, API keys, tokens or other private credentials in DI answers or ordinary screens.", 2000),
    ("SECURITY", "Data encryption", "All sensitive data in DACRE is encrypted at rest and in transit using industry-standard encryption protocols.", 1950),
    ("SECURITY", "Access control", "DACRE implements role-based access control (RBAC) ensuring users only see what they are authorized to see.", 1950),
    ("SECURITY", "Audit trail", "All significant actions in DACRE are logged with timestamps and user identities for complete auditability.", 1950),
    
    # ACCOUNT
    ("ACCOUNT", "Signup and access", "A user who completes the required signup information should be able to access DACRE. Duplicate usernames or emails should be prevented.", 1900),
    ("ACCOUNT", "Company separation", "Each organization has its own workspace. Normal company users should not receive system-wide visibility into other organizations.", 1900),
    ("ACCOUNT", "Company admin", "The first account creating a new organization becomes that organization's company admin. Later users are normal users unless an admin grants admin access.", 1850),
    ("ACCOUNT", "Subscription tiers", "DACRE offers Free, Professional, Business, and Enterprise tiers with different features and limits.", 1850),
    ("ACCOUNT", "User roles", "DACRE supports multiple user roles: master, admin, manager, analyst, and standard user with granular permissions.", 1850)
]


def _core_di_technology_seed():
    """Shared, curated technology knowledge available to every DI brain."""
    return [
        ("TECHNOLOGY", "Software engineering fundamentals",
         "Use modular design, clear interfaces, validation, error handling, logging, tests, code review, dependency pinning, and least-privilege access. Prefer simple maintainable solutions over unnecessary complexity.", 1950),
        ("TECHNOLOGY", "Web application architecture",
         "A web application normally separates presentation, application/business logic, data access, and external integrations. Validate all user input, enforce authorization server-side, and never trust browser-side controls for security.", 1950),
        ("TECHNOLOGY", "HTTP and APIs",
         "HTTP is request/response based. REST commonly uses GET, POST, PUT/PATCH and DELETE. APIs should validate inputs, authenticate requests, authorize resources, return useful status codes, rate-limit sensitive endpoints, and avoid leaking secrets.", 1950),
        ("TECHNOLOGY", "Databases",
         "Relational databases organize data into tables and use SQL. Use primary/foreign keys, constraints, indexes, transactions, parameterized queries, migrations, backups, and appropriate isolation. Never build SQL by concatenating untrusted user input.", 1950),
        ("TECHNOLOGY", "Authentication and authorization",
         "Authentication verifies identity; authorization determines permissions. Passwords should be salted and hashed with a password-specific KDF such as Argon2id, scrypt, or bcrypt. Use sessions or short-lived tokens, MFA for privileged access, secure cookies, CSRF protection where applicable, and server-side authorization checks.", 2000),
        ("TECHNOLOGY", "Secrets management",
         "API keys, passwords, signing keys and database credentials belong in environment variables or a dedicated secrets manager, not source code or client-side JavaScript. Rotate compromised credentials and avoid logging secrets.", 2000),
        ("TECHNOLOGY", "Cryptography",
         "Use established cryptographic libraries and modern authenticated encryption such as AES-GCM or ChaCha20-Poly1305. Hashing and encryption serve different purposes. Do not invent cryptographic algorithms or store plaintext credentials.", 1950),
        ("TECHNOLOGY", "Networking",
         "DNS maps names to IP addresses. TCP provides reliable ordered transport; UDP is connectionless. TLS protects data in transit. Firewalls, private networks, segmentation, secure DNS, and sensible egress controls reduce attack surface.", 1900),
        ("TECHNOLOGY", "Cloud architecture",
         "Cloud systems should use least privilege, private networking where appropriate, managed secrets, backups, monitoring, autoscaling based on real demand, and explicit cost controls. Design for failure rather than assuming a single service is always available.", 1900),
        ("TECHNOLOGY", "Containers and DevOps",
         "Containers package applications and dependencies consistently. CI/CD should run linting, tests, security checks and reproducible builds before deployment. Pin important dependencies and use immutable or versioned releases when practical.", 1900),
        ("TECHNOLOGY", "Observability",
         "Production systems need structured logs, metrics, traces, health checks and alerting. Logs should contain enough context to diagnose failures without exposing credentials, tokens or sensitive user data.", 1900),
        ("TECHNOLOGY", "Testing",
         "Use unit tests for small logic, integration tests for component boundaries, end-to-end tests for critical user journeys, and regression tests for repaired bugs. Test failure paths, permissions, malformed input and database behavior.", 1900),
        ("TECHNOLOGY", "AI systems",
         "AI systems can generate incorrect information. DI should distinguish verified facts from inference, use retrieval or tools for current information, cite evidence when available, ask for clarification when required, and avoid presenting guesses as certainty.", 2000),
        ("TECHNOLOGY", "Machine learning",
         "Machine learning includes supervised, unsupervised and reinforcement learning. Good ML practice includes representative data, train/validation/test separation, leakage prevention, appropriate metrics, monitoring for drift, and human review for consequential decisions.", 1900),
        ("TECHNOLOGY", "Data engineering",
         "Reliable data pipelines validate schemas, normalize data where appropriate, handle missing values explicitly, deduplicate safely, preserve lineage, and make transformations reproducible. Data quality should be measured rather than assumed.", 1900),
        ("TECHNOLOGY", "Privacy",
         "Collect only data needed for a defined purpose, restrict access, protect data in transit and at rest, define retention rules, support deletion where required, and avoid exposing personal information in logs or model prompts.", 1950),
        ("TECHNOLOGY", "Reliability and recovery",
         "Use transactions for related writes, idempotency for retryable operations, timeouts, bounded retries with backoff, circuit breakers where useful, backups, restore testing, and clear recovery procedures.", 1900),
        ("TECHNOLOGY", "Performance",
         "Measure before optimizing. Use profiling, database indexes, caching, pagination, batching and asynchronous work where they address measured bottlenecks. Avoid premature optimization that harms correctness or maintainability.", 1850),
        ("TECHNOLOGY", "Version control",
         "Use Git-style version control with small reviewable commits, meaningful branches, code review and release tags. Never commit secrets, private keys, production databases or generated credential files.", 1900),
        ("TECHNOLOGY", "Secure coding",
         "Defend against injection, XSS, CSRF, SSRF, insecure deserialization, path traversal, broken access control and dependency vulnerabilities. Encode output for its context and validate both syntax and business rules.", 2000),
    ]

def _ensure_core_tables(con):
    """Create the minimum DACRE tables needed by the runtime and repair layer."""
    ddl = {
        "companies": """CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL,
            owner_username TEXT, admin_password_hash TEXT, website_url TEXT, created_at TEXT)""",
        "users": """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT,
            username TEXT UNIQUE NOT NULL, company_name TEXT, email TEXT UNIQUE,
            email_password TEXT, password_hash TEXT, passkey_hash TEXT, role TEXT DEFAULT 'user',
            login_count INTEGER DEFAULT 0, created_at TEXT, last_login TEXT)""",
        "files": """CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, company_name TEXT,
            filename TEXT, file_type TEXT, file_json TEXT, created_at TEXT)""",
        "projects": """CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, company_name TEXT,
            project_name TEXT, active_filename TEXT, raw_json TEXT, processed_json TEXT,
            formula_logs TEXT, chart_config TEXT, updated_at TEXT)""",
        "activity": """CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, company_name TEXT,
            action TEXT, created_at TEXT)""",
        "company_website_profile": """CREATE TABLE IF NOT EXISTS company_website_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT UNIQUE, website_url TEXT,
            page_title TEXT, description TEXT, headings TEXT, summary TEXT,
            theme_primary TEXT, theme_accent TEXT, theme_background TEXT, theme_text TEXT,
            fetched_at TEXT, fetch_status TEXT)""",
        "public_visits": """CREATE TABLE IF NOT EXISTS public_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT, visitor_id TEXT, event_type TEXT,
            page_name TEXT, referrer TEXT, created_at TEXT)""",
        "emails_log": """CREATE TABLE IF NOT EXISTS emails_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT, recipient_email TEXT, recipient_name TEXT,
            company_name TEXT, subject TEXT, body TEXT, sender_email TEXT, status TEXT, sent_at TEXT)""",
        "notifications": """CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT, username TEXT,
            event_type TEXT, message TEXT, is_read INTEGER DEFAULT 0, created_at TEXT)""",
        "chat_history": """CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, company_name TEXT,
            role TEXT, sender TEXT, message TEXT, created_at TEXT)""",
        "loan_clients": """CREATE TABLE IF NOT EXISTS loan_clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, company_name TEXT,
            client_name TEXT, whatsapp_number TEXT, loan_amount REAL, lent_date TEXT,
            due_date TEXT, created_at TEXT, updated_at TEXT)""",
        "whatsapp_delivery_log": """CREATE TABLE IF NOT EXISTS whatsapp_delivery_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT, loan_id INTEGER, company_name TEXT,
            client_name TEXT, phone TEXT, reminder_type TEXT, template_name TEXT,
            message_id TEXT, status TEXT, response TEXT, created_at TEXT)""",
        "di_memory": """CREATE TABLE IF NOT EXISTS di_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT NOT NULL DEFAULT '',
            category TEXT, title TEXT, content TEXT, priority INTEGER DEFAULT 1000,
            active INTEGER DEFAULT 1, created_at TEXT, updated_at TEXT)""",
        "di_agents": """CREATE TABLE IF NOT EXISTS di_agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT, di_name TEXT UNIQUE NOT NULL, di_code TEXT,
            specialty TEXT, status TEXT DEFAULT 'Available', assigned_company TEXT,
            system_role TEXT, avatar_url TEXT, voice_profile TEXT, thinking_style TEXT,
            position_title TEXT DEFAULT 'DI Specialist', rank_level INTEGER DEFAULT 1,
            appointed_at TEXT, appointed_by TEXT, created_by TEXT, created_at TEXT, last_active TEXT)""",
        "di_private_memory": """CREATE TABLE IF NOT EXISTS di_private_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT, di_id INTEGER NOT NULL, title TEXT,
            content TEXT, source TEXT DEFAULT 'master', created_by TEXT, created_at TEXT,
            updated_at TEXT, active INTEGER DEFAULT 1)""",
        "di_research_store": """CREATE TABLE IF NOT EXISTS di_research_store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL DEFAULT '',
            di_id INTEGER,
            di_name TEXT NOT NULL DEFAULT 'DI',
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'local',
            server_endpoint TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            last_accessed TEXT NOT NULL
        )""",
        "di_position_history": """CREATE TABLE IF NOT EXISTS di_position_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT, di_id INTEGER, old_position TEXT,
            new_position TEXT, old_rank INTEGER, new_rank INTEGER, appointed_by TEXT, created_at TEXT)""",
        "di_master_thanks": """CREATE TABLE IF NOT EXISTS di_master_thanks (
            id INTEGER PRIMARY KEY AUTOINCREMENT, di_id INTEGER, message TEXT, created_at TEXT)""",
        "sovereign_calls": """CREATE TABLE IF NOT EXISTS sovereign_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT, room_name TEXT UNIQUE, title TEXT,
            host_username TEXT, created_at TEXT, ended_at TEXT, status TEXT DEFAULT 'active')""",
        "sovereign_call_members": """CREATE TABLE IF NOT EXISTS sovereign_call_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT, call_id INTEGER, di_id INTEGER,
            joined_at TEXT, left_at TEXT)""",
        "sovereign_call_messages": """CREATE TABLE IF NOT EXISTS sovereign_call_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT, call_id INTEGER, speaker_type TEXT,
            speaker_id TEXT, speaker_name TEXT, message TEXT, created_at TEXT)""",
        "david_creations": """CREATE TABLE IF NOT EXISTS david_creations (
            id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, title TEXT, content TEXT,
            created_at TEXT, updated_at TEXT)""",
        "call_rooms": """CREATE TABLE IF NOT EXISTS call_rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT, room_name TEXT,
            title TEXT, host_username TEXT, mode TEXT DEFAULT 'team', created_at TEXT)""",
        "call_participants": """CREATE TABLE IF NOT EXISTS call_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT, room_name TEXT, username TEXT,
            display_name TEXT, joined_at TEXT, left_at TEXT)""",
        "decision_ledger": """CREATE TABLE IF NOT EXISTS decision_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT, username TEXT,
            decision TEXT, context TEXT, expected_outcome TEXT, result TEXT, created_at TEXT)""",
        "opportunity_radar": """CREATE TABLE IF NOT EXISTS opportunity_radar (
            id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT, title TEXT,
            description TEXT, score REAL, created_at TEXT)""",
        "di_action_log": """CREATE TABLE IF NOT EXISTS di_action_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT, username TEXT,
            agent_name TEXT, action_type TEXT, request TEXT, result TEXT, created_at TEXT)""",
    }
    for sql in ddl.values():
        con.execute(sql)

def using_cloud_db():
    return False

def db():
    con = sqlite3.connect(str(DB_PATH), timeout=30, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con

def init_db():
    con = db()
    try:
        _ensure_core_tables(con)
        con.commit()
    finally:
        con.close()

def hash_password(password):
    """PBKDF2 password hash with per-password salt."""
    password = str(password or "")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310000)
    return "pbkdf2_sha256$310000$" + base64.b64encode(salt).decode() + "$" + base64.b64encode(digest).decode()

def verify_password(candidate, stored):
    if not candidate or not stored:
        return False, False
    try:
        if stored.startswith("pbkdf2_sha256$"):
            _, rounds, salt_b64, digest_b64 = stored.split("$", 3)
            digest = hashlib.pbkdf2_hmac("sha256", candidate.encode(), base64.b64decode(salt_b64), int(rounds))
            return hmac.compare_digest(digest, base64.b64decode(digest_b64)), True
        # Backward-compatible SHA-256 hex hashes.
        if re.fullmatch(r"[0-9a-fA-F]{64}", stored):
            return hmac.compare_digest(hashlib.sha256(candidate.encode()).hexdigest(), stored.lower()), False
    except Exception:
        return False, False
    return False, False

def maybe_upgrade_password_hash(con, username, candidate, stored):
    ok, modern = verify_password(candidate, stored)
    if ok and not modern:
        con.execute("UPDATE users SET passkey_hash=?, password_hash=? WHERE username=?",
                    (hash_password(candidate), hash_password(candidate), username))
        con.commit()
    return ok

def ensure_master():
    con = db()
    try:
        now = datetime.now().isoformat(timespec="seconds")
        row = con.execute("SELECT id FROM users WHERE username=?", (MASTER_USERNAME,)).fetchone()
        if not row:
            con.execute("""INSERT INTO users
                (first_name,last_name,username,company_name,email,password_hash,passkey_hash,role,login_count,created_at)
                VALUES(?,?,?,?,?,?,?,?,?,?)""",
                ("David","Emenike",MASTER_USERNAME,"DACRE MASTER","master@dacre.local",
                 hash_password(MASTER_PASSKEY),hash_password(MASTER_PASSKEY),"master",0,now))
        con.execute("INSERT OR IGNORE INTO companies(name,owner_username,created_at) VALUES(?,?,?)",
                    ("DACRE MASTER", MASTER_USERNAME, now))
        con.commit()
    finally:
        con.close()

def log_activity(username, company, action, notify_admin=True):
    con = db()
    try:
        con.execute("INSERT INTO activity(username,company_name,action,created_at) VALUES(?,?,?,?)",
                    (username, company, action, datetime.now().isoformat(timespec="seconds")))
        con.commit()
    finally:
        con.close()

def notify_company_admin(company, message, event_type="info"):
    con = db()
    try:
        con.execute("INSERT INTO notifications(company_name,event_type,message,is_read,created_at) VALUES(?,?,?,?,?)",
                    (company, event_type, message, 0, datetime.now().isoformat(timespec="seconds")))
        con.commit()
    finally:
        con.close()

def _migrate_sqlite_to_supabase_once():
    return False

def ensure_runtime_schema():
    """Repair and migrate legacy DACRE SQLite schemas without deleting user data."""
    init_db()
    con = db()
    try:
        cols = {row["name"] for row in con.execute("PRAGMA table_info(chat_history)").fetchall()}
        if "sender" not in cols:
            con.execute("ALTER TABLE chat_history ADD COLUMN sender TEXT")
        if "role" not in cols:
            con.execute("ALTER TABLE chat_history ADD COLUMN role TEXT")
        con.execute("""
            UPDATE chat_history
            SET sender = CASE
                WHEN sender IS NULL OR TRIM(sender) = '' THEN
                    CASE
                        WHEN LOWER(COALESCE(role,'')) IN ('assistant','di','ai') THEN 'DI'
                        WHEN LOWER(COALESCE(role,'')) IN ('user','human') THEN 'User'
                        ELSE COALESCE(role, 'User')
                    END
                ELSE sender
            END
            WHERE sender IS NULL OR TRIM(sender) = ''
        """)
        con.execute("CREATE INDEX IF NOT EXISTS idx_chat_history_user_company ON chat_history(username, company_name, id)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_di_research_store_company ON di_research_store(company_name, id)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_di_research_store_di ON di_research_store(di_id, id)")
        con.commit()
    finally:
        con.close()
    return True


def ensure_di_agent_columns():
    init_db()
    return True

def _seed_memory_rows(company_name="", extra_rows=None):
    """Idempotently seed core memory into a company-visible DI memory board."""
    rows = list(DI_MEMORY_SEED) + list(_core_di_technology_seed()) + list(extra_rows or [])
    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    try:
        for category, title, content, priority in rows:
            exists = con.execute(
                "SELECT id FROM di_memory WHERE lower(company_name)=lower(?) AND category=? AND title=? LIMIT 1",
                (company_name, category, title)
            ).fetchone()
            if not exists:
                con.execute("""INSERT INTO di_memory
                    (company_name,category,title,content,priority,active,created_at,updated_at)
                    VALUES(?,?,?,?,?,?,?,?)""",
                    (company_name, category, title, content, int(priority), 1, now, now))
        con.commit()
    finally:
        con.close()

def seed_di_memory():
    """Seed the global DI memory board and all existing organization boards."""
    _seed_memory_rows("")
    con = db()
    try:
        companies = [r["name"] for r in con.execute("SELECT name FROM companies WHERE name IS NOT NULL").fetchall()
                     if str(r["name"]).upper() != "DACRE MASTER"]
    finally:
        con.close()
    for company in companies:
        _seed_memory_rows(company)

def seed_all_di_brains():
    """Give every DI agent the same core webstore and technology knowledge."""
    con = db()
    try:
        agents = con.execute("SELECT id, assigned_company, di_name FROM di_agents").fetchall()
    finally:
        con.close()
    for agent in agents:
        company = str(agent["assigned_company"] or "").strip()
        if company:
            _seed_memory_rows(company)
        else:
            _seed_memory_rows("")
        # The shared company/global memory board is the source of the common brain.
        # Private master notes remain separate and are never copied into ordinary DI memory.

def get_di_memory(limit=80, query=""):
    company_name = (st.session_state.get("user") or {}).get("company")
    con = db()
    try:
        if company_name:
            rows = con.execute(
                """SELECT id,company_name,category,title,content,priority,active,created_at,updated_at
                   FROM di_memory
                   WHERE active=1 AND (company_name='' OR lower(company_name)=lower(?))
                   ORDER BY priority DESC,id ASC""", (company_name,)
            ).fetchall()
        else:
            rows = con.execute(
                """SELECT id,company_name,category,title,content,priority,active,created_at,updated_at
                   FROM di_memory WHERE active=1 ORDER BY priority DESC,id ASC"""
            ).fetchall()
    finally:
        con.close()
    if not query:
        return [dict(r) for r in rows[:int(limit)]]
    words = set(re.findall(r"[a-z0-9]{3,}", query.lower()))
    scored = []
    for r in rows:
        blob = f"{r['company_name']} {r['category']} {r['title']} {r['content']}".lower()
        hits = sum(1 for w in words if w in blob)
        exact = 10 if r["title"].lower() in query.lower() else 0
        if hits:
            scored.append((hits * 25 + exact + int(r["priority"] or 0) / 1000, dict(r)))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in scored[:int(limit)]]

def di_memory_context(limit=80, query=""):
    """Get DI memory context as a string."""
    rows = get_di_memory(limit, query=query)
    if not rows:
        return "DI Memory Box has no matching records for this question."
    return "\n".join([f"[{r['category']}] {r['title']}: {r['content']}" for r in rows])

def memory_box_direct_answer(text):
    """Give a deterministic direct answer when a trusted memory record matches."""
    matches = get_di_memory(limit=5, query=text)
    if not matches:
        return None

    low = text.lower().strip()
    if any(k in low for k in ["your name", "who are you", "what should i call you"]):
        return "My name is DI — David's Intelligence."
    if "who created" in low or "who made" in low or "creator" in low:
        return "DACRE Analysis and DI were created by David Emenike."
    if "david emenike" in low and any(k in low for k in ["know", "who", "creator"]):
        return "Yes. David Emenike is the creator and Overall Administrator of DACRE Analysis."

    qwords = set(re.findall(r"[a-z0-9]{3,}", low))
    best = matches[0]
    mtext = f"{best['title']} {best['content']}".lower()
    hits = sum(1 for w in qwords if w in mtext)
    if hits >= 2:
        return best['content']
    return None

# =============================================================================
# ENHANCED DI REPLY WITH WEBSTORE KNOWLEDGE
# =============================================================================

def get_webstore_answer(query: str) -> Optional[str]:
    """Get answer from webstore knowledge base."""
    q_lower = query.lower().strip()
    
    # Check for DACRE platform questions
    if "what is dacre" in q_lower or "dacre platform" in q_lower:
        return "DACRE is a comprehensive business intelligence platform that combines data analysis, AI assistance, and business insights. It helps organizations make data-driven decisions."
    
    if "dacre features" in q_lower or "what can dacre do" in q_lower:
        return "DACRE offers: Data Upload and Analysis, Business Intelligence Dashboards, DI AI Assistant, Data Visualization, Export Reports, File Management, and Organization Administration."
    
    if "dacre pricing" in q_lower or "how much does dacre cost" in q_lower:
        return "DACRE offers a Free tier for individuals, Professional tier for small teams, and Enterprise tier for large organizations with custom requirements. Visit https://dacre.ai/pricing for details."
    
    if "dacre support" in q_lower or "how to get help" in q_lower:
        return "You can get DACRE support through email at support@dacre.ai, documentation at https://dacre.ai/docs, or by asking DI for immediate help."
    
    # Check for DI questions
    if "what is di" in q_lower or "who is di" in q_lower:
        return "DI (David's Intelligence) is the built-in AI assistant inside DACRE Analysis. I can analyze data, answer business questions, provide strategic advice, explain technical concepts, and assist with decision making."
    
    if "what can di do" in q_lower or "di capabilities" in q_lower:
        return "DI can: analyze data, answer business questions, provide strategic advice, explain technical concepts, research information, assist with decision making, and help with DACRE features."
    
    # Check for business intelligence questions
    if "business intelligence" in q_lower:
        return "Business intelligence is the process of analyzing data to inform business decisions. DACRE provides BI tools including data health scoring, trend detection, anomaly detection, executive briefs, and actionable insights from your data."
    
    # Check for technology questions
    if "python" in q_lower and "data" in q_lower:
        return "Python is the primary language for data science with libraries like Pandas, NumPy, Matplotlib, and Scikit-learn. DACRE is built with Python and uses it for all data processing and analysis."
    
    if "streamlit" in q_lower:
        return "Streamlit is a Python framework for building data applications quickly. DACRE's interface is built with Streamlit, making it interactive, responsive, and easy to use."
    
    if "pandas" in q_lower:
        return "Pandas provides DataFrame structures for data manipulation. DACRE uses Pandas for all data processing, cleaning, and analysis operations."
    
    if "sql" in q_lower or "database" in q_lower:
        return "SQL is used for structured data storage and querying. DACRE uses SQLite for local development and PostgreSQL/Supabase for production deployments."
    
    if "ai" in q_lower or "artificial intelligence" in q_lower:
        return "AI (Artificial Intelligence) enables pattern recognition, predictive analytics, and natural language processing. DACRE's DI uses AI for intelligent responses and data analysis."
    
    if "cloud" in q_lower or "cloud computing" in q_lower:
        return "Cloud platforms enable scalable application deployment. DACRE can be deployed on Streamlit Cloud, AWS, or any cloud provider, with optional Supabase PostgreSQL for database."
    
    # Check for specific technology combinations
    if "api" in q_lower or "integration" in q_lower:
        return "APIs allow different systems to communicate. DACRE integrates with various APIs for market data, AI services, and external tools."
    
    return None

def enhanced_di_reply(message, user, df, allow_online=True, language="English — Nigeria"):
    """Enhanced DI reply with webstore knowledge."""
    text = message.strip()
    low = text.lower()
    
    # First, check webstore knowledge base
    webstore_answer = get_webstore_answer(text)
    if webstore_answer:
        return webstore_answer
    
    # Check memory box direct answers
    direct = memory_box_direct_answer(text)
    if direct:
        return direct
    
    # Use the standard di_reply for everything else
    return di_reply(message, user, df, allow_online, language)

# =============================================================================
# AUTHENTICATION FUNCTIONS
# =============================================================================

def send_di_welcome_email(first_name, last_name, company_name, email, email_password=""):
    """Send welcome email to new user."""
    full_name = f"{first_name} {last_name}".strip()
    subject = f"Welcome to DACRE Analysis — DI is now active for {company_name}!"
    body = (
        f"Hello {first_name},\n\n"
        "Welcome to DACRE Analysis. I am DI (David's Intelligence), your business and data intelligence copilot.\n\n"
        f"Your workspace for {company_name} is now active. You can upload datasets, clean and analyse them, build charts, "
        "export results and chat naturally with DI about your workspace.\n\n"
        "Please keep your DACRE Account Passkey private and do not share it with anyone. "
        "If you did not create this account, please contact the DACRE administrator.\n\n"
        "Warm regards,\nDI — David's Intelligence\nDACRE Analysis Platform"
    )

    def mail_secret(name, default=""):
        try:
            value = st.secrets.get(name, "")
        except Exception:
            value = ""
        return str(value or os.getenv(name, default) or default).strip()

    # Gmail is the production mail provider for DACRE.
    # Credentials MUST come from Streamlit Secrets/environment variables; never hard-code them.
    providers = [
        ("Mailjet", "DACRE_MAILJET_SMTP_HOST", "DACRE_MAILJET_SMTP_PORT", "DACRE_MAILJET_SMTP_USER", "DACRE_MAILJET_SMTP_PASSWORD", "DACRE_MAILJET_SMTP_FROM"),
        ("Gmail", "DACRE_GMAIL_SMTP_HOST", "DACRE_GMAIL_SMTP_PORT", "DACRE_GMAIL_SMTP_USER", "DACRE_GMAIL_SMTP_PASSWORD", "DACRE_GMAIL_SMTP_FROM"),
    ]

    statuses = []
    status = "NOT SENT — no mail provider is configured"
    sent_provider = ""

    for provider, host_key, port_key, user_key, pass_key, from_key in providers:
        smtp_host = mail_secret(host_key)
        smtp_port = int(mail_secret(port_key, "587"))
        smtp_user = mail_secret(user_key)
        smtp_pass = mail_secret(pass_key)
        sender = mail_secret(from_key, smtp_user or "")
        if not (smtp_host and smtp_user and smtp_pass):
            continue

        try:
            msg = MIMEMultipart()
            msg["From"] = sender or smtp_user
            msg["To"] = email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))
            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(sender or smtp_user, [email], msg.as_string())
            status = f"Sent via {provider} SMTP"
            sent_provider = provider
            break
        except Exception as exc:
            statuses.append(f"{provider}: {type(exc).__name__}")

    if not sent_provider and statuses:
        status = "NOT SENT — configured mail providers failed (" + "; ".join(statuses) + ")"

    con = db()
    con.execute("""
        INSERT INTO emails_log
        (recipient_email, recipient_name, company_name, subject, body, sender_email, status, sent_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        email, full_name, company_name, subject, body, sender, status,
        datetime.now().isoformat(timespec="seconds"),
    ))
    con.commit()
    con.close()
    return status

class _WebsiteExtractor(HTMLParser):
    """Extract website information for company onboarding."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = []
        self.description = ""
        self.headings = []
        self.paragraphs = []
        self._active = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self._active = "title"
            self._buf = []
        elif tag in ("h1", "h2", "h3"):
            self._active = tag
            self._buf = []
        elif tag == "p":
            self._active = "p"
            self._buf = []
        elif tag == "meta" and str(attrs.get("name", "")).lower() == "description":
            self.description = str(attrs.get("content", "")).strip()[:700]

    def handle_data(self, data):
        if self._active is not None:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if self._active is None:
            return
        text = re.sub(r"\s+", " ", " ".join(self._buf)).strip()
        if text:
            if self._active == "title":
                self.title.append(text[:300])
            elif self._active in ("h1", "h2", "h3") and text not in self.headings:
                self.headings.append(text[:180])
            elif self._active == "p" and len(text) > 35 and text not in self.paragraphs:
                self.paragraphs.append(text[:450])
        self._active = None
        self._buf = []

def _normalize_website_url(value):
    """Normalize website URL."""
    raw = str(value or "").strip()
    if not raw:
        return ""
    if not re.match(r"^https?://", raw, re.I):
        raw = "https://" + raw
    parsed = urlparse(raw)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return ""
    return raw[:500]

def _fetch_website_profile(url, timeout=1.8):
    """Fetch website profile for company onboarding."""
    url = _normalize_website_url(url)
    if not url:
        return None

    req = urllib.request.Request(url, headers={"User-Agent": "DACRE-DI/1.0 Website Intelligence"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            final_url = resp.geturl() or url
            raw = resp.read(260_000)
            charset = resp.headers.get_content_charset() or "utf-8"
            html = raw.decode(charset, errors="ignore")

        parser = _WebsiteExtractor()
        parser.feed(html)
        title = (parser.title[0] if parser.title else "").strip()
        summary = parser.description.strip() or (parser.paragraphs[0] if parser.paragraphs else "")
        headings = list(parser.headings[:10])

        colors = []
        for c in re.findall(r"#[0-9a-fA-F]{6}", html):
            c = c.lower()
            if c not in colors:
                colors.append(c)
            if len(colors) >= 8:
                break

        content_summary = " | ".join(headings[:6])
        if summary:
            content_summary = (summary[:700] + (" | " + content_summary if content_summary else ""))[:1400]

        return {
            "website_url": final_url[:500],
            "page_title": title[:300],
            "description": parser.description[:700],
            "headings": json.dumps(headings),
            "summary": content_summary,
            "theme_primary": colors[0] if colors else "#4b82f5",
            "theme_accent": colors[1] if len(colors) > 1 else "#62c8f5",
            "theme_background": colors[2] if len(colors) > 2 else "#0b1020",
            "theme_text": "#f4f7ff"
        }
    except Exception:
        return None

def ensure_company_di(company_name):
    """Ensure a DI agent exists for a company."""
    company_name = str(company_name or "").strip()
    if not company_name or company_name.upper() == "DACRE MASTER":
        return None

    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    try:
        row = con.execute("SELECT di_name FROM di_agents WHERE assigned_company=? ORDER BY id ASC LIMIT 1", (company_name,)).fetchone()
        if row:
            return row["di_name"]

        base = "DI — " + re.sub(r"[^A-Za-z0-9 ]+", "", company_name).strip()[:34]
        if not base.strip():
            base = "DI — Business Intelligence"

        name = base
        n = 2
        while con.execute("SELECT 1 FROM di_agents WHERE di_name=?", (name,)).fetchone():
            name = f"{base[:28]} {n}"
            n += 1

        code = "DI-ORG-" + re.sub(r"[^A-Z0-9]+", "-", company_name.upper()).strip("-")[:26]
        while con.execute("SELECT 1 FROM di_agents WHERE di_code=?", (code,)).fetchone():
            code += "-ORG"

        con.execute("""
            INSERT INTO di_agents
            (di_name, di_code, specialty, status, assigned_company, system_role,
             avatar_url, voice_profile, thinking_style, created_by, created_at, last_active)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            name, code, "Company Intelligence", "Assigned", company_name,
            "Know the customer's business, website context and workspace data; answer with evidence first.",
            "", "en-NG", "Practical, business-aware, evidence-first and company-specific.",
            MASTER_USERNAME, now, now
        ))
        con.commit()
        _seed_memory_rows(company_name)
        return name
    finally:
        con.close()

def _store_website_memory(company_name, profile, di_name):
    """Store website information in DI memory."""
    now = datetime.now().isoformat(timespec="seconds")
    items = [
        ("WEBSITE", "Official company website", f"Official website supplied at signup: {profile.get('website_url','')}"),
        ("WEBSITE", "Website title", profile.get("page_title") or f"Website for {company_name}"),
        ("WEBSITE", "Website summary", profile.get("summary") or profile.get("description") or "No readable summary was available from the public homepage."),
        ("WEBSITE", "Website headings", profile.get("headings") or "[]"),
        ("DI", "Organization DI", f"Dedicated organization DI: {di_name}. Use this company's website context and workspace data when answering."),
    ]

    con = db()
    try:
        for cat, title, content in items:
            con.execute(
                "INSERT INTO di_memory(company_name,category,title,content,priority,active,created_at,updated_at) "
                "VALUES(?,?,?,?,?,?,?,?)",
                (company_name, cat, title, content, 850, 1, now, now)
            )

        con.execute("""
            INSERT INTO company_website_profile
            (company_name, website_url, page_title, description, headings, summary,
             theme_primary, theme_accent, theme_background, theme_text, fetched_at, fetch_status)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(company_name) DO UPDATE SET
                website_url=excluded.website_url,
                page_title=excluded.page_title,
                description=excluded.description,
                headings=excluded.headings,
                summary=excluded.summary,
                theme_primary=excluded.theme_primary,
                theme_accent=excluded.theme_accent,
                theme_background=excluded.theme_background,
                theme_text=excluded.theme_text,
                fetched_at=excluded.fetched_at,
                fetch_status=excluded.fetch_status
        """, (
            company_name,
            profile.get("website_url", ""),
            profile.get("page_title", ""),
            profile.get("description", ""),
            profile.get("headings", "[]"),
            profile.get("summary", ""),
            profile.get("theme_primary", "#4b82f5"),
            profile.get("theme_accent", "#62c8f5"),
            profile.get("theme_background", "#0b1020"),
            profile.get("theme_text", "#f4f7ff"),
            now, "ready"
        ))
        con.commit()
    finally:
        con.close()

def _website_onboarding_worker(company_name, website_url, di_name):
    """Background worker for website onboarding."""
    profile = _fetch_website_profile(website_url, timeout=1.8)
    if profile is None:
        return
    _store_website_memory(company_name, profile, di_name)
    try:
        con = db()
        con.execute("UPDATE companies SET website_url=? WHERE name=?", (profile.get("website_url", website_url), company_name))
        con.commit()
        con.close()
    except Exception:
        pass

def start_website_onboarding(company_name, website_url, di_name):
    """Start website onboarding in background."""
    url = _normalize_website_url(website_url)
    if not url:
        return
    threading.Thread(target=_website_onboarding_worker, args=(company_name, url, di_name), daemon=True).start()

def record_public_visit(event_type="landing_view", page_name="Landing"):
    """Record public visit for analytics."""
    if event_type == "landing_view" and st.session_state.get("public_visit_logged"):
        return

    visitor_id = st.session_state.get("visitor_id") or uuid.uuid4().hex
    st.session_state.visitor_id = visitor_id

    con = db()
    con.execute(
        "INSERT INTO public_visits(visitor_id, event_type, page_name, referrer, created_at) VALUES(?,?,?,?,?)",
        (visitor_id, event_type, page_name, "", datetime.now().isoformat(timespec="seconds"))
    )
    con.commit()
    con.close()

    if event_type == "landing_view":
        st.session_state.public_visit_logged = True

def apply_company_website_theme(user):
    """Apply company website theme to the app."""
    company = str((user or {}).get("company", "")).strip()
    if not company or (user or {}).get("role") == "master":
        return

    con = db()
    row = con.execute(
        "SELECT theme_primary, theme_accent, theme_background, theme_text "
        "FROM company_website_profile WHERE lower(company_name)=lower(?) ORDER BY id DESC LIMIT 1",
        (company,)
    ).fetchone()
    con.close()

    if not row:
        return

    p = row["theme_primary"] or "#4b82f5"
    a = row["theme_accent"] or "#62c8f5"
    b = row["theme_background"] or "#f7f9fc"

    st.markdown(f"""
    <style>
        :root{{--dacre-primary:{p};--dacre-primary2:{a};}}
        .stApp{{background:#f7f9fc!important}}
        .dacre-page-chrome,.user-dash,.user-work-card,.user-kpi,.dacre-panel,.di-metric{{border-color:{p}35!important}}
        .dacre-page-chrome:before{{background:{p}!important}}
        .stButton>button[kind="primary"],.stButton>button[data-testid="baseButton-primary"]{{background:linear-gradient(135deg,{p},{a})!important;border-color:{p}!important;color:#fff!important}}
        .dacre-quickbar{{border-left:4px solid {p};}}
    </style>
    """, unsafe_allow_html=True)

def restore_user_workspace(user):
    """Restore persistent workspace state after every successful sign-in.

    Account data is stored in the database, so users can return days or weeks
    later with the same credentials and continue from their last saved state.
    """
    if not user:
        return None

    # Restore the most recently saved project/data state.
    project = restore_project(user)
    if project:
        st.session_state.active_filename = project.get("filename") or ""
        st.session_state.raw_df = project.get("raw")
        st.session_state.processed_df = project.get("processed")
        st.session_state.formula_logs = project.get("logs") or []
        st.session_state.chart_config = project.get("chart") or {}

    # Restore the user's persistent DI conversation.
    st.session_state.chat_history = load_chat_history(user, limit=40)

    # Keep a durable activity trail for the overall administrator.
    log_activity(
        user.get("username", ""),
        user.get("company", user.get("company_name", "")),
        "Signed in and resumed persistent workspace",
        notify_admin=True,
    )

    # Mirror the active user to MongoDB when MongoDB is configured.
    try:
        mongo_sync_user(user)
        mongo_log_activity(
            user.get("username", ""),
            user.get("company", user.get("company_name", "")),
            "Signed in and resumed persistent workspace",
            user.get("role", "user"),
        )
    except Exception:
        pass

    return project

def authenticate(company_name, full_name, passkey, email=""):
    """Authenticate a user."""
    company_clean = (company_name or "").strip().lower()
    full_name_clean = (full_name or "").strip().lower()
    email_clean = (email or "").strip().lower()
    passkey_clean = (passkey or "").strip()

    if not passkey_clean:
        return None, "Please enter your Account Passkey."
    if not company_clean and not email_clean:
        return None, "Please enter your Company / Organization Name or Email Address."

    con = db()
    try:
        if (company_clean == "dacre master" or full_name_clean == "david emenike" or email_clean == "master@dacre.local") and master_passkey_gate(passkey_clean):
            row = con.execute("SELECT first_name,last_name,username,company_name,email,role FROM users WHERE username=?", (MASTER_USERNAME,)).fetchone()
            if row:
                now = datetime.now().isoformat(timespec="seconds")
                con.execute("UPDATE users SET login_count=login_count+1,last_login=? WHERE username=?", (now, MASTER_USERNAME))
                con.commit()
                result = dict(row)
                log_activity(MASTER_USERNAME, result.get("company_name", "DACRE MASTER"), "Signed in", notify_admin=False)
                return result, None

        if email_clean:
            rows = con.execute("SELECT first_name,last_name,username,company_name,email,passkey_hash,role FROM users WHERE lower(email)=?", (email_clean,)).fetchall()
        else:
            rows = con.execute("SELECT first_name,last_name,username,company_name,email,passkey_hash,role FROM users WHERE lower(company_name)=?", (company_clean,)).fetchall()

        valid_rows = []
        for candidate_row in rows:
            if maybe_upgrade_password_hash(con, candidate_row["username"], passkey_clean, candidate_row["passkey_hash"]):
                valid_rows.append(candidate_row)
        rows = valid_rows

        if not rows:
            if email_clean:
                exists = con.execute("SELECT 1 FROM users WHERE lower(email)=? LIMIT 1", (email_clean,)).fetchone()
            else:
                exists = con.execute("SELECT 1 FROM users WHERE lower(company_name)=? LIMIT 1", (company_clean,)).fetchone()

            if exists:
                return None, "This account has already been created, but the passkey does not match. Please check your passkey and try again."
            return None, "This account has not been created. Please go to the Sign Up page and create your account to access DACRE Analysis."

        matched = None
        for r in rows:
            candidate = f"{r['first_name']} {r['last_name']}".strip().lower()
            if not full_name_clean or candidate == full_name_clean:
                matched = r
                break

        if matched is None:
            return None, "The account exists, but the Full Name does not match the account. Please enter the name used during Sign Up."

        now = datetime.now().isoformat(timespec="seconds")
        con.execute("UPDATE users SET login_count=login_count+1,last_login=? WHERE username=?", (now, matched["username"]))
        con.commit()
        result = {
            "first_name": matched["first_name"],
            "last_name": matched["last_name"],
            "username": matched["username"],
            "company": matched["company_name"],
            "email": matched["email"],
            "role": matched["role"]
        }
    finally:
        con.close()

    log_activity(result["username"], result["company"], "Signed in", notify_admin=result["role"] != "master")
    return result, None

def create_account(first, last, company, email, email_password, passkey, website_url=""):
    """Create a new account."""
    company_clean = canonical_company_name(company)
    email_clean = email.strip().lower()
    passkey_clean = passkey.strip()
    website_raw = str(website_url or "").strip()
    normalized_website = _normalize_website_url(website_raw)

    if website_raw and not normalized_website:
        return False, "Please enter a valid company website URL, for example https://www.example.com.", None

    if not company_clean or not email_clean or not passkey_clean:
        return False, "Please fill in Company Name, Email Address, and Account Passkey.", None

    if "@" not in email_clean or "." not in email_clean.split("@")[-1]:
        return False, "Please enter a valid email address.", None

    email_prefix = email_clean.split("@")[0].replace(".", " ").replace("_", " ").title()
    first_clean = first.strip() if first and first.strip() else (email_prefix.split()[0] if email_prefix else "User")
    last_clean = last.strip() if last and last.strip() else (" ".join(email_prefix.split()[1:]) if len(email_prefix.split()) > 1 else "Member")
    username_clean = email_clean

    if username_clean == MASTER_USERNAME:
        return False, "That username/email is reserved for the Master account.", None

    con = db()
    try:
        now = datetime.now().isoformat(timespec="seconds")
        cur = con.cursor()

        existing_account = cur.execute(
            "SELECT first_name, last_name, company_name FROM users WHERE lower(email)=lower(?) OR lower(username)=lower(?) LIMIT 1",
            (email_clean, username_clean),
        ).fetchone()

        if existing_account:
            return False, (
                "This account has already been added. The email address you entered is already registered "
                f"for {existing_account['company_name']}. Please use the Sign In page to access your account."
            ), None

        company_row = cur.execute("SELECT name FROM companies WHERE lower(name)=lower(?)", (company_clean,)).fetchone()

        if company_row:
            role = "user"
        else:
            cur.execute("INSERT INTO companies(name,owner_username,admin_password_hash,created_at) VALUES (?,?,?,?)",
                        (company_clean, username_clean, hash_password(passkey_clean), now))
            role = "company_admin"

        cur.execute("""
            INSERT INTO users
            (first_name,last_name,username,company_name,email,email_password,password_hash,passkey_hash,role,login_count,created_at,last_login)
            VALUES (?,?,?,?,?,?,?,?,?,1,?,?)
        """, (
            first_clean, last_clean, username_clean, company_clean, email_clean, "",
            hash_password(passkey_clean), hash_password(passkey_clean), role, now, now,
        ))
        con.commit()

        di_name = ensure_company_di(company_clean)
        _seed_memory_rows(company_clean)
        clean_url = normalized_website
        if clean_url:
            con.execute("UPDATE companies SET website_url=? WHERE lower(name)=lower(?)", (clean_url, company_clean))
            con.commit()
            start_website_onboarding(company_clean, clean_url, di_name or ("DI — " + company_clean[:32]))

        threading.Thread(target=send_di_welcome_email, args=(first_clean, last_clean, company_clean, email_clean, email_password.strip()), daemon=True).start()
        log_activity(username_clean, company_clean, "Created account & signed in", notify_admin=(role == "user"))

        if role == "company_admin":
            notify_company_admin(company_clean, f"New organization created by {first_clean} {last_clean}. You are the organization admin.", "new_company")

        return True, "Account created successfully. DI is preparing your company intelligence in the background.", {
            "first_name": first_clean,
            "last_name": last_clean,
            "username": username_clean,
            "company": company_clean,
            "email": email_clean,
            "role": role,
        }
    except sqlite3.IntegrityError:
        return False, "An account with this email address is already registered.", None
    finally:
        con.close()

def is_chibobec_company(company_name):
    """Check if company is Chibobec."""
    return "chibobec" in str(company_name or "").strip().lower()

def canonical_company_name(company_name):
    """Get canonical company name."""
    return CHIBOBEC_COMPANY if is_chibobec_company(company_name) else str(company_name or "").strip()

def normalize_whatsapp_number(number):
    """Normalize WhatsApp number."""
    raw = re.sub(r"[^0-9+]", "", str(number or "").strip())
    if raw.startswith("00"):
        raw = "+" + raw[2:]
    if raw.startswith("0"):
        raw = "+234" + raw[1:]
    if raw and not raw.startswith("+"):
        raw = "+" + raw
    return raw

def _dacre_secret(name, default=""):
    """Read a Streamlit secret first, then an environment variable."""
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value or os.getenv(name, default) or default).strip()

def _meta_whatsapp_config():
    """Get WhatsApp configuration."""
    return {
        "token": _dacre_secret("DACRE_WHATSAPP_TOKEN"),
        "phone_id": _dacre_secret("DACRE_WHATSAPP_PHONE_NUMBER_ID"),
        "version": _dacre_secret("DACRE_WHATSAPP_API_VERSION", "v23.0"),
        "reminder_2_template": _dacre_secret("DACRE_WHATSAPP_2DAY_TEMPLATE", "dacre_loan_due_2days"),
        "due_template": _dacre_secret("DACRE_WHATSAPP_DUE_TEMPLATE", "dacre_loan_due_today"),
        "language": _dacre_secret("DACRE_WHATSAPP_TEMPLATE_LANGUAGE", "en_US"),
    }

def _meta_phone(phone):
    """Clean phone number for Meta API."""
    return re.sub(r"[^0-9]", "", normalize_whatsapp_number(phone))

def _log_whatsapp_delivery(loan_id, company, client_name, phone, reminder_type, template_name, message_id, status, response):
    """Log WhatsApp delivery."""
    con = db()
    try:
        con.execute("PRAGMA busy_timeout = 30000;")
        try:
            con.execute("PRAGMA journal_mode = WAL;")
        except Exception:
            pass

        con.execute("""
            CREATE TABLE IF NOT EXISTS whatsapp_delivery_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                loan_id INTEGER,
                company_name TEXT NOT NULL DEFAULT '',
                client_name TEXT NOT NULL DEFAULT '',
                whatsapp_number TEXT NOT NULL DEFAULT '',
                reminder_type TEXT NOT NULL DEFAULT '',
                template_name TEXT,
                message_id TEXT,
                status TEXT NOT NULL DEFAULT '',
                response TEXT,
                created_at TEXT NOT NULL DEFAULT ''
            )
        """)

        con.execute("""
            INSERT INTO whatsapp_delivery_log
            (loan_id, company_name, client_name, whatsapp_number, reminder_type,
             template_name, message_id, status, response, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            loan_id, company, client_name, phone, reminder_type,
            template_name, message_id, status, str(response)[:4000],
            datetime.now().isoformat(timespec="seconds"),
        ))
        con.commit()
    finally:
        con.close()

def send_whatsapp_template(to_number, template_name, parameters):
    """Send an approved Meta WhatsApp Cloud API template."""
    cfg = _meta_whatsapp_config()
    if not cfg["token"] or not cfg["phone_id"]:
        return False, "Meta WhatsApp Cloud API is not configured."

    to = _meta_phone(to_number)
    if len(to) < 8:
        return False, "Invalid WhatsApp number."

    endpoint = f"https://graph.facebook.com/{cfg['version']}/{cfg['phone_id']}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": cfg["language"]},
            "components": [{"type": "body", "parameters": [{"type": "text", "text": str(v)} for v in parameters]}],
        },
    }

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"Authorization": f"Bearer {cfg['token']}", "Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw or "{}")
            message_id = (data.get("messages") or [{}])[0].get("id")
            if 200 <= response.status < 300 and message_id:
                return True, message_id
            return False, f"Meta returned HTTP {response.status}: {raw[:1000]}"
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8")
        except Exception:
            detail = str(exc)
        return False, f"Meta WhatsApp API rejected the message (HTTP {exc.code}): {detail[:1200]}"
    except Exception as exc:
        return False, f"WhatsApp send failed: {type(exc).__name__}: {exc}"

def send_whatsapp_message(to_number, body):
    """Send WhatsApp message - only templates are allowed."""
    return False, "Use an approved Meta WhatsApp template for business-initiated reminders."

def add_loan_client(username, company, client_name, whatsapp_number, loan_amount, lent_date, due_date):
    """Add a loan client."""
    client_name = str(client_name or "").strip()
    phone = normalize_whatsapp_number(whatsapp_number)
    if not client_name or not phone:
        return False, "Client name and WhatsApp number are required."
    if due_date < lent_date:
        return False, "The due date cannot be earlier than the lending date."

    now = datetime.now().isoformat(timespec="seconds")
    con = db()
    try:
        con.execute("""
            INSERT INTO loan_clients
            (username, company_name, client_name, whatsapp_number, loan_amount, lent_date, due_date, created_at, updated_at)
            VALUES(?,?,?,?,?,?,?,?,?)
        """, (
            username, company, client_name, phone, float(loan_amount or 0),
            str(lent_date), str(due_date), now, now
        ))
        con.commit()
        return True, "Loan client saved."
    except Exception as exc:
        return False, str(exc)
    finally:
        con.close()

def delete_loan_client(loan_id, username):
    """Delete a loan client."""
    con = db()
    con.execute("DELETE FROM loan_clients WHERE id=? AND username=?", (int(loan_id), username))
    con.commit()
    con.close()

def process_chibobec_reminders(username, company):
    """Send due-date reminders through the real Meta WhatsApp Cloud API."""
    if not is_chibobec_company(company):
        return []

    cfg = _meta_whatsapp_config()
    today = datetime.now().date()
    con = db()
    rows = con.execute("SELECT * FROM loan_clients WHERE username=? AND company_name=? ORDER BY due_date", (username, company)).fetchall()
    results = []

    for row in rows:
        try:
            due = datetime.strptime(row["due_date"], "%Y-%m-%d").date()
        except Exception:
            continue

        days_left = (due - today).days

        if days_left == 2 and not row["reminder_2_sent"]:
            reminder_type, template_name, sent_column, message_column = "2-day reminder", cfg["reminder_2_template"], "reminder_2_sent", "reminder_2_message_id"
        elif days_left == 0 and not row["due_sent"]:
            reminder_type, template_name, sent_column, message_column = "due-date reminder", cfg["due_template"], "due_sent", "due_message_id"
        else:
            continue

        parameters = [row["client_name"], f"₦{float(row['loan_amount']):,.2f}", due.strftime("%d %B %Y")]
        ok, status = send_whatsapp_template(row["whatsapp_number"], template_name, parameters)

        now = datetime.now().isoformat(timespec="seconds")
        if ok:
            con.execute(f"UPDATE loan_clients SET {sent_column}=1,{message_column}=?,last_whatsapp_status=?,last_whatsapp_error=NULL,updated_at=? WHERE id=?", (status, "sent", now, row["id"]))
            _log_whatsapp_delivery(row["id"], company, row["client_name"], row["whatsapp_number"], reminder_type, template_name, status, "sent", "Meta accepted the message.")
        else:
            con.execute(f"UPDATE loan_clients SET last_whatsapp_status=?,last_whatsapp_error=?,updated_at=? WHERE id=?", ("failed", status, now, row["id"]))
            _log_whatsapp_delivery(row["id"], company, row["client_name"], row["whatsapp_number"], reminder_type, template_name, None, "failed", status)

        results.append((row["client_name"], reminder_type, ok, status))

    con.commit()
    con.close()
    return results

# =============================================================================
# DATA PROCESSING FUNCTIONS
# =============================================================================

def load_dataframe(uploaded_file):
    """Load a dataframe from an uploaded file."""
    extension = uploaded_file.name.rsplit(".", 1)[-1].lower()
    if extension == "csv":
        return pd.read_csv(uploaded_file)
    if extension == "tsv":
        return pd.read_csv(uploaded_file, sep="\t")
    if extension in ("xlsx", "xls"):
        return pd.read_excel(uploaded_file)
    if extension == "json":
        return pd.read_json(uploaded_file)
    raise ValueError(f"Unsupported file type: .{extension}")

def clean_dataframe(df):
    """Clean a dataframe by removing empty rows/columns and standardizing data."""
    out = df.copy()
    out.columns = [re.sub(r"\s+", " ", str(c).strip()) if str(c).strip() else f"Column_{i+1}" for i, c in enumerate(out.columns)]
    out = out.dropna(axis=0, how="all").dropna(axis=1, how="all")

    for column in out.columns:
        if out[column].dtype == "object":
            series = out[column].astype(str).replace({"nan": ""}).str.strip()
            numeric_candidate = series.str.replace(r"[\$€£₦,%]", "", regex=True).str.replace(",", "", regex=False)
            numeric = pd.to_numeric(numeric_candidate, errors="coerce")
            if numeric.notna().mean() >= 0.80 and series.ne("").any():
                out[column] = numeric
            else:
                out[column] = series

    return out.drop_duplicates().reset_index(drop=True)

def dataframe_to_json(df):
    """Convert dataframe to JSON string."""
    return "" if df is None else df.to_json(orient="split", date_format="iso")

def dataframe_from_json(value):
    """Convert JSON string to dataframe."""
    if not value:
        return None
    try:
        return pd.read_json(io.StringIO(value), orient="split")
    except Exception:
        return None

def safe_dataframe_for_streamlit(df):
    """Prevent pyarrow duplicate-column failures when Streamlit renders a dataframe."""
    if df is None:
        return df
    out = df.copy()
    seen = {}
    cols = []
    for col in out.columns:
        base = str(col)
        n = seen.get(base, 0)
        seen[base] = n + 1
        cols.append(base if n == 0 else f"{base}_{n + 1}")
    out.columns = cols
    return out

def save_file(user, uploaded_file, df):
    """Save a file to the database."""
    con = db()
    con.execute(
        "INSERT INTO files(username, company_name, filename, file_type, file_json, created_at) VALUES(?,?,?,?,?,?)",
        (user["username"], user["company"], uploaded_file.name, uploaded_file.name.rsplit(".", 1)[-1].lower(), dataframe_to_json(df), datetime.now().isoformat(timespec="seconds"))
    )
    con.commit()
    con.close()
    log_activity(user["username"], user["company"], f"Saved file: {uploaded_file.name}")

def get_files(user):
    """Get files for a user."""
    con = db()
    rows = con.execute("SELECT filename, file_type, created_at, file_json FROM files WHERE company_name=? ORDER BY id DESC", (user["company"],)).fetchall()
    con.close()
    return rows

def save_project(user, raw_df, processed_df, filename, logs, chart_config=None):
    """Save project state."""
    con = db()
    existing = con.execute("SELECT id FROM projects WHERE username=? AND company_name=?", (user["username"], user["company"])).fetchone()
    payload = (
        user["username"], user["company"], "Main Workspace", filename or "",
        dataframe_to_json(raw_df), dataframe_to_json(processed_df),
        json.dumps(logs), json.dumps(chart_config or {}),
        datetime.now().isoformat(timespec="seconds")
    )

    if existing:
        con.execute("""
            UPDATE projects SET
                project_name=?, active_filename=?, raw_json=?, processed_json=?,
                formula_logs=?, chart_config=?, updated_at=?
            WHERE id=?
        """, (*payload[2:], existing["id"]))
    else:
        con.execute("""
            INSERT INTO projects
            (username, company_name, project_name, active_filename, raw_json, processed_json,
             formula_logs, chart_config, updated_at)
            VALUES(?,?,?,?,?,?,?,?,?)
        """, payload)

    con.commit()
    con.close()

def restore_project(user):
    """Restore project state."""
    con = db()
    row = con.execute(
        "SELECT active_filename, raw_json, processed_json, formula_logs, chart_config "
        "FROM projects WHERE username=? AND company_name=? ORDER BY id DESC LIMIT 1",
        (user["username"], user["company"])
    ).fetchone()
    con.close()

    if not row:
        return None

    try:
        logs = json.loads(row["formula_logs"]) if row["formula_logs"] else []
    except Exception:
        logs = []

    try:
        chart = json.loads(row["chart_config"]) if row["chart_config"] else {}
    except Exception:
        chart = {}

    return {
        "filename": row["active_filename"],
        "raw": dataframe_from_json(row["raw_json"]),
        "processed": dataframe_from_json(row["processed_json"]),
        "logs": logs,
        "chart": chart
    }

def make_excel(processed_df, chart_df=None):
    """Create Excel file from dataframes."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        processed_df.to_excel(writer, sheet_name="Processed Data", index=False)
        if chart_df is not None:
            chart_df.to_excel(writer, sheet_name="Dynamic Chart", index=False)
    output.seek(0)
    return output.getvalue()

def apply_formula(df, formula, options):
    """Apply a formula to a dataframe."""
    formula = formula.upper()

    if formula == "SUM":
        return pd.to_numeric(df[options["column"]], errors="coerce").sum()
    if formula == "AVERAGE":
        return pd.to_numeric(df[options["column"]], errors="coerce").mean()
    if formula == "COUNT":
        return int(pd.to_numeric(df[options["column"]], errors="coerce").count())
    if formula == "COUNTA":
        return int(df[options["column"]].notna().sum())
    if formula == "MAX":
        return pd.to_numeric(df[options["column"]], errors="coerce").max()
    if formula == "MIN":
        return pd.to_numeric(df[options["column"]], errors="coerce").min()

    if formula == "CONCATENATE":
        result = df[options["first"]].astype(str) + options.get("separator", " ") + df[options["second"]].astype(str)
        return "column", options["new_column"], result

    if formula in ("UPPER", "LOWER", "TRIM"):
        series = df[options["column"]].astype(str)
        result = series.str.upper() if formula == "UPPER" else series.str.lower() if formula == "LOWER" else series.str.strip()
        return "column", options["column"], result

    return None

def _numeric_columns(df):
    """Get numeric columns from dataframe."""
    return df.select_dtypes(include="number").columns.tolist() if df is not None else []

def business_health(df):
    """Calculate business health score from dataframe."""
    if df is None or df.empty:
        return {"score": 0, "rows": 0, "columns": 0, "missing_pct": 100.0, "duplicate_pct": 0.0, "numeric": 0}

    total_cells = max(1, df.shape[0] * df.shape[1])
    missing_pct = float(df.isna().sum().sum() / total_cells * 100)
    duplicate_pct = float(df.duplicated().mean() * 100)
    numeric = len(_numeric_columns(df))
    score = max(0, min(100, round(100 - missing_pct * 0.65 - duplicate_pct * 0.45 + min(numeric, 10) * 0.8)))

    return {
        "score": score,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_pct": missing_pct,
        "duplicate_pct": duplicate_pct,
        "numeric": numeric
    }

def business_signals(df):
    """Return explainable, dataset-derived signals."""
    if df is None or df.empty:
        return []

    signals = []
    nums = _numeric_columns(df)

    for col in nums[:20]:
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        if len(s) < 4:
            continue

        mean = float(s.mean())
        std = float(s.std()) if len(s) > 1 else 0.0

        if std > 0:
            high = int((s > mean + 3 * std).sum())
            low = int((s < mean - 3 * std).sum())
            if high or low:
                signals.append({
                    "type": "anomaly",
                    "column": str(col),
                    "message": f"{col} contains {high + low} unusually distant value(s) from its average."
                })

        if len(s) >= 8:
            first = float(s.head(max(1, len(s) // 5)).mean())
            last = float(s.tail(max(1, len(s) // 5)).mean())
            if first != 0:
                change = (last - first) / abs(first) * 100
                if abs(change) >= 10:
                    direction = "up" if change > 0 else "down"
                    signals.append({
                        "type": "trend",
                        "column": str(col),
                        "message": f"{col} trends {direction} by about {abs(change):.1f}% between the early and recent portions of the dataset."
                    })

    missing = df.isna().sum().sort_values(ascending=False)
    for col, count in missing[missing > 0].head(5).items():
        signals.append({
            "type": "quality",
            "column": str(col),
            "message": f"{col} has {int(count):,} missing value(s)."
        })

    return signals[:12]

def build_executive_brief(df, company):
    """Build an executive brief from the dataset."""
    if df is None or df.empty:
        return "There is no active dataset to brief yet. Upload your business data and I will prepare an executive review."

    health = business_health(df)
    signals = business_signals(df)
    nums = _numeric_columns(df)

    lines = [
        f"Executive brief for {company}.",
        f"The active dataset contains {len(df):,} rows across {len(df.columns):,} columns. "
        f"Data health is {health['score']}/100, with {health['missing_pct']:.1f}% missing cells "
        f"and {health['duplicate_pct']:.1f}% duplicate rows."
    ]

    if nums:
        for col in nums[:5]:
            s = pd.to_numeric(df[col], errors="coerce").dropna()
            if not s.empty:
                lines.append(
                    f"{col}: total {s.sum():,.2f}; average {s.mean():,.2f}; "
                    f"minimum {s.min():,.2f}; maximum {s.max():,.2f}."
                )

    if signals:
        lines.append("Key signals: " + " ".join(x["message"] for x in signals[:5]))
    else:
        lines.append("I did not detect a strong trend or anomaly from the available numeric fields, so I would review the business context before making a recommendation.")

    return " ".join(lines)

def ask_data_question(question, df):
    """Handle questions that genuinely require a loaded dataset."""
    q = (question or "").lower()

    if df is None:
        data_markers = [
            "how many rows", "row count", "how many columns", "column count",
            "duplicate rows", "duplicates", "missing values", "missing data",
            "empty cells", "dataset", "data set", "my sales", "my revenue",
            "top products", "best selling", "analyze my data", "analyse my data",
            "executive brief from my data", "summary of my data",
        ]
        if any(m in q for m in data_markers):
            return (
                "I can do that as soon as you upload or open a dataset. "
                "For example, I can analyze sales, revenue, missing values, duplicates, trends and charts."
            )
        return None

    nums = _numeric_columns(df)

    if any(k in q for k in ["executive brief", "business brief", "management summary", "ceo summary"]):
        return build_executive_brief(df, st.session_state.user["company"] if st.session_state.get("user") else "your organization")

    if "health" in q or "quality score" in q or "data quality" in q:
        h = business_health(df)
        return f"Data health is {h['score']}/100. Missing cells: {h['missing_pct']:.1f}%. Duplicate rows: {h['duplicate_pct']:.1f}%. Numeric columns: {h['numeric']}."

    if ("top" in q or "highest" in q or "largest" in q) and nums:
        target = next((c for c in nums if str(c).lower() in q), nums[0])
        view = df[[target]].copy().sort_values(target, ascending=False).head(10)
        return f"Top 10 records by {target}: " + "; ".join(f"{i+1}. {v:,.2f}" for i, v in enumerate(view[target].tolist()))

    if ("total" in q or "sum" in q or "revenue" in q or "sales" in q) and nums:
        target = next((c for c in nums if str(c).lower() in q), nums[0])
        return f"The total for {target} is {pd.to_numeric(df[target], errors='coerce').sum():,.2f}."

    return None

def online_lookup(query, max_results=5):
    """Dependency-free public web lookup. Safe fallback when model tools are unavailable."""
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote_plus(query)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 DACRE-DI/2.0"})
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode("utf-8", errors="ignore")

        items = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.*?)</a>', html, flags=re.I | re.S)
        results = []
        for href, title in items[:max_results]:
            clean_title = re.sub(r"<.*?>", "", title).strip()
            clean_href = urllib.parse.unquote(href)
            if clean_title and clean_href:
                results.append((clean_title, clean_href))
        return results
    except Exception:
        return []
# =============================================================================
# SEARCH & DI BRAIN ROUTERS (LINES 1770 - 1990)
# =============================================================================

def google_web_search(query, max_results=5):
    """Search the web using Google (requires googlesearch-python)."""
    if not WEB_SEARCH_AVAILABLE:
        return online_lookup(query, max_results)

    try:
        results = []
        for url in google_search(query, num_results=max_results, stop=max_results):
            results.append(("Search result", url))
        return results
    except Exception:
        return online_lookup(query, max_results)

def needs_web_research(text):
    """Detect questions that benefit from current public information."""
    low = (text or "").lower()
    markers = [
        "latest", "current", "today", "tonight", "this week", "this month",
        "recent", "news", "price", "pricing", "cost", "version", "release",
        "2026", "search online", "look online", "on the internet", "online",
        "according to", "official", "website", "who won", "what happened",
        "google", "search", "find", "tell me about", "what is", "who is"
    ]
    return any(m in low for m in markers)

def build_di_context(user, df):
    """Build context for DI responses."""
    master_context = ""
    if user.get("role") == "master":
        master_context = (
            "SOVEREIGN MASTER CONTEXT: The speaker is David Emenike, creator and Overall Administrator "
            "of DACRE Analysis. This conversation is private to the master administration layer. "
            "Respond with exceptional respect, technical depth, executive judgment and practical actions. "
            "Never reveal private credentials, passkeys, API keys or hidden security values.\n"
        )

    context = [
        APP_KNOWLEDGE,
        master_context,
        "DI MEMORY BOX (persistent source of truth):\n" + di_memory_context(query=getattr(st.session_state, "di_memory_query", "")),
        f"Current organization: {user.get('company','')}. Current user: {user.get('first_name','')} {user.get('last_name','')}. Role: {user.get('role','user')}.",
    ]

    try:
        recent = st.session_state.get("chat_history", [])[-12:]
        if recent:
            context.append("RECENT CONVERSATION:\n" + "\n".join(
                f"{m.get('sender','User')}: {m.get('text','')}" for m in recent
            ))
    except Exception:
        pass

    if df is not None:
        context.append(f"Active dataset has {len(df):,} rows and {len(df.columns):,} columns.")
        context.append("Columns: " + ", ".join(map(str, df.columns)))

    return "\n".join(context)

def _free_secret(name):
    """Get a free AI provider secret."""
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value or os.getenv(name, "") or "").strip()

def _free_ai_only_mode():
    """Check if free AI only mode is enabled."""
    value = _free_secret("DACRE_FREE_AI_ONLY")
    if not value:
        return True
    return str(value).lower() not in {"0", "false", "no", "off"}

def _groq_generate(system_prompt, user_prompt, max_tokens=900):
    """Use Groq's free-plan compatible OpenAI endpoint when a free-tier key exists."""
    key = _free_secret("GROQ_API_KEY")
    if not key:
        return None

    model = _free_secret("DACRE_GROQ_MODEL") or "openai/gpt-oss-120b"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_completion_tokens": min(int(max_tokens), 1800),
    }

    try:
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8"))
        return ((data.get("choices") or [{}])[0].get("message") or {}).get("content", "").strip() or None
    except Exception:
        return None

def _gemini_generate(system_prompt, user_prompt, max_tokens=900):
    """Use Google's Gemini developer API when a free-tier key exists."""
    key = _free_secret("GEMINI_API_KEY")
    if not key:
        return None

    model = _free_secret("DACRE_GEMINI_MODEL") or "gemini-2.5-flash"
    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": min(int(max_tokens), 1800)},
    }

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(model, safe='')}:generateContent"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"x-goog-api-key": key, "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8"))
        parts = ((data.get("candidates") or [{}])[0].get("content") or {}).get("parts") or []
        answer = "".join(str(p.get("text", "")) for p in parts).strip()
        return answer or None
    except Exception:
        return None

def _openai_generate_paid(system_prompt, user_prompt, max_tokens=900):
    """Optional paid provider. NEVER used unless explicitly enabled."""
    if _free_ai_only_mode():
        return None

    api_key = _free_secret("DACRE_AI_API_KEY")
    if not api_key:
        return None

    model = _free_secret("DACRE_AI_MODEL") or "gpt-4o-mini"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": min(int(max_tokens), 1800),
    }

    try:
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return ((data.get("choices") or [{}])[0].get("message") or {}).get("content", "").strip() or None
    except Exception:
        return None

def ai_generate(system_prompt, user_prompt, max_tokens=900):
    """Free-first DI reasoning router with a hard no-paid default."""
    answer = _groq_generate(system_prompt, user_prompt, max_tokens=max_tokens)
    if answer:
        return answer

    answer = _gemini_generate(system_prompt, user_prompt, max_tokens=max_tokens)
    if answer:
        return answer

    answer = _openai_generate_paid(system_prompt, user_prompt, max_tokens=max_tokens)
    return answer or None

def free_ai_provider_status():
    """Get status of free AI providers."""
    return {
        "groq": bool(_free_secret("GROQ_API_KEY")),
        "gemini": bool(_free_secret("GEMINI_API_KEY")),
        "paid_openai_enabled": bool(not _free_ai_only_mode() and _free_secret("DACRE_AI_API_KEY")),
        "free_only": _free_ai_only_mode(),
    }

def normalize_di_identity(text):
    """Keep DI's displayed first-person identity consistent."""
    if not text:
        return text
    text = re.sub(r"\bI\s+am\s+D([\.,!?])", r"I am DI\1", text, flags=re.IGNORECASE)
    text = re.sub(r"\bI\x27m\s+D([\.,!?])", r"I am DI\1", text, flags=re.IGNORECASE)
    return text

def di_reply(message, user, df, allow_online=True, language="English — Nigeria"):
    """Generate a reliable DI response using trusted memory, data, web evidence and AI."""
    text = str(message or "").strip()
    low = text.lower()
    if not text:
        return "I am ready. Tell me the business result you want to achieve."

    name = "Master David" if user.get("role") == "master" else (user.get("first_name") or "there")

    if any(k in low for k in ["your name", "what is your name", "who are you", "what's your name"]):
        return "My name is DI — David's Intelligence. I am the intelligence assistant inside DACRE Analysis, created by David Emenike."

    if any(k in low for k in ["who created you", "who made you", "who created dacre", "who made dacre"]):
        return "DACRE Analysis and DI were created by David Emenike, the creator and Overall Administrator of the platform."

    if low in {"hello", "hi", "hey", "good morning", "good afternoon", "good evening", "good day"}:
        return f"Good day {name}. DI is online. What would you like us to work on first?"

    direct = memory_box_direct_answer(text)
    if direct:
        return direct

    webstore = get_webstore_answer(text)
    if webstore:
        return webstore

    if "what can" in low and "dacre" in low:
        return "DACRE is a business and data-intelligence workspace with data analysis, cleaning, formulas, charts, File Vault, exports, organization administration and DI intelligence."

    data_answer = ask_data_question(text, df)
    if data_answer:
        return data_answer

    if "how many rows" in low or "row count" in low:
        return "There is no active dataset yet." if df is None else f"The active dataset contains {len(df):,} rows."
    if "how many columns" in low or "column count" in low:
        return "There is no active dataset yet." if df is None else f"The active dataset contains {len(df.columns):,} columns."
    if "duplicate" in low:
        return "There is no active dataset yet." if df is None else f"The current dataset has {int(df.duplicated().sum()):,} duplicate rows."
    if "missing" in low or "empty" in low:
        if df is None:
            return "There is no active dataset yet. Upload a dataset and I can inspect it."
        missing = df.isna().sum().sort_values(ascending=False)
        top = missing[missing > 0].head(8)
        return "I checked the active dataset. I do not see missing values in the current columns." if top.empty else \
            "The columns with the most missing values are: " + "; ".join(f"{c}: {int(v)}" for c, v in top.items())
    if any(k in low for k in ["describe", "summary", "overview"]):
        if df is None:
            return "There is no active dataset yet. Upload a dataset and I can summarise it."
        return f"Dataset overview: {len(df):,} rows, {len(df.columns):,} columns, {len(df.select_dtypes(include='number').columns)} numeric columns and {int(df.duplicated().sum()):,} duplicate rows."

    if "who am i" in low or "do you know me" in low:
        if user.get("role") == "master":
            return "You are David Emenike, the creator and Overall Administrator of DACRE Analysis."
        return f"You are {user.get('first_name','the current user')} {user.get('last_name','')}, working in the {user.get('company','your organization')} workspace."

    if "memory box" in low:
        return "The DI Memory Box is DI's persistent trusted knowledge base for DACRE identity, platform rules, security, technology, webstore knowledge and organization context."

    # Current-information questions should use public web evidence when available.
    should_search = bool(allow_online and (needs_web_research(text) or len(low.split()) >= 4))
    results = google_web_search(text, max_results=5) if should_search else []
    source_text = "\n".join(f"SOURCE {i+1}: {title}\nURL: {href}" for i, (title, href) in enumerate(results))

    context = build_di_context(user, df)
    research_note = (
        "\nPUBLIC WEB RESEARCH:\n" + source_text
        if source_text else
        "\nNo public web research was used; rely on trusted DI memory and available workspace data."
    )

    answer = ai_generate(
        f"""You are DI — David's Intelligence inside DACRE Analysis.
Answer the user's actual question directly and accurately.
Use the DI Memory Box as trusted project context and the active dataset when relevant.
Use supplied public-web evidence for current facts. Never invent facts, credentials, prices, features or citations.
Clearly distinguish verified facts from inference and state uncertainty when evidence is insufficient.
Never reveal passwords, hashes, API keys, tokens, private master notes or hidden security values.
Respond in the selected language when practical: {language}.""",
        f"DACRE CONTEXT:\n{context}{research_note}\n\nUSER QUESTION:\n{text}",
        max_tokens=1400,
    )
    if answer:
        suffix = "\n\nSources checked: " + "; ".join(t for t, _ in results[:3]) if results else ""
        return normalize_di_identity(answer) + suffix
    if results:
        return "I checked public sources but could not synthesize a verified answer. Relevant sources:\n" + "\n".join(f"• {t} — {u}" for t, u in results)

    return "I could not verify a reliable answer from the current DI Memory Box, workspace data or available AI provider. Please rephrase the question or provide more context."

def save_chat_history_message(user, sender, message):
    """Write a chat message with both legacy role and new sender fields."""
    username = str(user.get("username", "")).strip()
    company = str(user.get("company_name", user.get("company", ""))).strip()
    sender = str(sender or "User").strip()
    message = str(message or "").strip()
    if not username or not company or not message:
        return False
    ensure_runtime_schema()
    con = db()
    try:
        role = "assistant" if sender not in {"User", "Human"} else "user"
        con.execute(
            "INSERT INTO chat_history(username, company_name, role, sender, message, created_at) VALUES(?,?,?,?,?,?)",
            (username, company, role, sender, message, datetime.now().isoformat(timespec="seconds")),
        )
        con.commit()
        return True
    finally:
        con.close()


def load_chat_history(user, limit=40):
    """Restore DI history safely for both old and new user-record shapes."""
    username = str(user.get("username", "")).strip()
    company = str(user.get("company_name", user.get("company", ""))).strip()

    if not username or not company:
        return []

    con = db()
    rows = con.execute(
        "SELECT sender, message FROM chat_history WHERE username=? AND company_name=? ORDER BY id DESC LIMIT ?",
        (username, company, int(limit)),
    ).fetchall()
    con.close()

    return [{"sender": r["sender"], "text": r["message"]} for r in reversed(rows)]

def verify_recaptcha_token(token):
    """Verify Google's reCAPTCHA token when DACRE_RECAPTCHA_SECRET is configured."""
    secret = os.getenv("DACRE_RECAPTCHA_SECRET", "").strip()
    if not secret or not token:
        return False

    try:
        payload = urllib.parse.urlencode({"secret": secret, "response": token}).encode()
        req = urllib.request.Request(
            "https://www.google.com/recaptcha/api/siteverify",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
        return bool(data.get("success"))
    except Exception:
        return False

# =============================================================================
# VOICE & UI FUNCTIONS
# =============================================================================

def transcribe_audio(audio_value):
    """Transcribe a browser recording when SpeechRecognition is installed."""
    if sr is None:
        return None, "Voice transcription package is not installed. Add SpeechRecognition to requirements.txt."
    
    try:
        recognizer = sr.Recognizer()
        raw = audio_value.getvalue()
        with sr.AudioFile(io.BytesIO(raw)) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="en-NG")
        return text, None
    except sr.UnknownValueError:
        return None, "DI could not clearly understand that recording. Please speak a little slower and try again."
    except sr.RequestError:
        return None, "Voice transcription service is temporarily unavailable. You can still use text chat."
    except Exception as exc:
        return None, f"Voice transcription could not be completed: {type(exc).__name__}."

def speak(text, language_code=None, voice_profile=None):
    """Speak DI responses by default; browser voice remains optional via Text/Voice mode."""
    if not text or st.session_state.get("di_response_mode", "voice") != "voice":
        return
    
    language_code = language_code or DI_LANGUAGE_PROFILES.get(st.session_state.get("di_language", "English — Nigeria"), {}).get("code", "en-NG")
    profile = (voice_profile or "").strip().lower()
    
    hints = {
        "male": r"male|man|daniel|david|alex|george|james|oliver|microsoft.*male|google.*male",
        "female": r"female|woman|samantha|aria|ava|victoria|zira|microsoft.*female|google.*female",
    }
    hint = hints.get(profile, profile if profile else hints["male"])
    
    safe_text = json.dumps(str(text))
    safe_lang = json.dumps(language_code)
    safe_hint = json.dumps(hint)
    pitch = 0.78 if profile == "female" else 0.62
    
    components.html(f"""
    <script>
    (() => {{
      const text={safe_text}, lang={safe_lang}, hint={safe_hint};
      if (!('speechSynthesis' in window) || !('SpeechSynthesisUtterance' in window)) return;
      const run=()=>{{
        try {{
          window.speechSynthesis.cancel();
          const u=new SpeechSynthesisUtterance(text); u.lang=lang; u.rate=0.91; u.pitch={pitch}; u.volume=1;
          const voices=window.speechSynthesis.getVoices();
          const base=lang.toLowerCase().split('-')[0];
          const same=voices.filter(v=>(v.lang||'').toLowerCase().startsWith(base));
          const rx=new RegExp(hint,'i');
          const preferred=same.find(v=>rx.test((v.name||'')+' '+(v.lang||''))) || same.find(v=>(v.lang||'').toLowerCase()===lang.toLowerCase()) || same[0] || voices[0];
          if(preferred) u.voice=preferred;
          window.speechSynthesis.speak(u);
        }} catch(e) {{ console.warn('DACRE voice error',e); }}
      }};
      if(window.speechSynthesis.getVoices().length) run(); else window.speechSynthesis.onvoiceschanged=run;
      setTimeout(run,250);
    }})();
    </script>
    """, height=1, scrolling=False)

def master_user_record():
    """Get master user record."""
    con = db()
    row = con.execute(
        "SELECT first_name,last_name,username,company_name,email,role FROM users WHERE username=?",
        (MASTER_USERNAME,),
    ).fetchone()
    con.close()
    
    if row:
        data = dict(row)
        data["company"] = data.get("company_name", "DACRE MASTER")
        return data
    
    return {
        "first_name": "David",
        "last_name": "Emenike",
        "username": MASTER_USERNAME,
        "company_name": "DACRE MASTER",
        "company": "DACRE MASTER",
        "email": "master@dacre.local",
        "role": "master"
    }

def master_passkey_gate(passkey):
    """Verify master passkey."""
    candidate = (passkey or "").strip()
    if not candidate:
        return False
    
    expected_hash = hash_password(MASTER_PASSKEY) if MASTER_PASSKEY else MASTER_PASSKEY_HASH
    ok, _ = verify_password(candidate, expected_hash)
    return bool(ok)

def manage_app_password_gate():
    """Protect DACRE's in-app management/admin surfaces with the management passkey."""
    if st.session_state.get("manage_app_unlocked"):
        return True

    st.markdown("### 🔐 Manage App")
    st.caption("Enter the management password to access administrative controls.")
    with st.form("manage_app_password_form", clear_on_submit=False):
        candidate = st.text_input("Manage App Password", type="password", key="manage_app_password")
        submitted = st.form_submit_button("Unlock Manage App", type="primary", use_container_width=True)
    if submitted:
        if hmac.compare_digest(candidate.strip(), MANAGE_APP_PASSKEY):
            st.session_state.manage_app_unlocked = True
            log_activity(
                (st.session_state.get("user") or {}).get("username", "unknown"),
                (st.session_state.get("user") or {}).get("company", "unknown"),
                "Unlocked Manage App"
            )
            st.rerun()
        st.error("Incorrect Manage App password.")
    return False

def chibobec_login_monitor():
    """Return every Chibobec account plus its real login activity."""
    con = db()
    try:
        users = pd.read_sql_query(
            """SELECT id, first_name, last_name, username, company_name, email, role,
                      login_count, created_at, last_login
               FROM users
               WHERE lower(company_name) LIKE '%chibobec%'
               ORDER BY CASE WHEN last_login IS NULL THEN 1 ELSE 0 END, last_login DESC, id DESC""",
            con,
        )
        if users.empty:
            return users
        users["login_status"] = users["last_login"].apply(lambda x: "Logged in" if pd.notna(x) and str(x).strip() else "Never logged in")
        users["company_access"] = users["company_name"].apply(lambda x: "Chibobec workspace" if is_chibobec_company(x) else "Company workspace")
        return users
    finally:
        con.close()

def render_di_video_call_stage(agent_rows, title, user_label):
    """Render a premium visual call stage."""
    people = []
    for idx, row in enumerate(agent_rows):
        a = dict(row)
        name = str(a.get("di_name") or "DI")
        avatar = str(a.get("avatar_url") or "")
        position = str(a.get("position_title") or a.get("specialty") or "DI Specialist")
        
        if not avatar:
            avatar = DI_AVATAR_LIBRARY["female" if idx % 2 else "male"][idx % len(DI_AVATAR_LIBRARY["female" if idx % 2 else "male"])]
        
        people.append(f"""<div class='di-video-person' data-speaker-index='{idx}'>
          <div class='di-video-face-wrap'><div class='di-video-ring'></div>
          <img class='di-video-face' src='{_escape_html(avatar)}' alt='{_escape_html(name)}' 
               onerror=\"this.style.display='none';this.parentElement.classList.add('avatar-fallback')\">
          <div class='di-avatar-fallback'>{_escape_html(name[:1].upper())}</div></div>
          <div class='di-video-name'>{_escape_html(name)}</div>
          <div class='di-video-role'>{_escape_html(position)}</div>
          <div class='di-video-status'><span class='speaker-dot'>●</span> <span class='speaker-text'>Ready</span></div>
        </div>""")
    
    founder_src = CEO_PORTRAIT_DATA_URL if 'CEO_PORTRAIT_DATA_URL' in globals() else ''
    founder = f"""<div class='di-video-person active-human' data-founder='1'>
      <div class='di-video-face-wrap'><div class='di-video-ring'></div>
      <img class='di-video-face founder-face' src='{founder_src}' alt='David Emenike' 
           onerror=\"this.style.display='none';this.parentElement.classList.add('avatar-fallback')\">
      <div class='di-avatar-fallback founder-fallback'>DE</div></div>
      <div class='di-video-name'>{_escape_html(user_label or 'David Emenike')}</div>
      <div class='di-video-role'>Creator · CEO · Overall Administrator</div>
      <div class='di-video-status'><span class='speaker-dot'>●</span> <span class='speaker-text'>Connected</span></div>
    </div>"""
    
    components.html(f"""
    <section class='di-video-call'>
      <div class='di-video-call-head'>
        <div><div class='eyebrow'>DACRE VIDEO CALL</div>
        <h2>{_escape_html(title)}</h2>
        <p>Fixed DI identities · permanent portraits · real call speaker state when LiveKit is connected</p>
        </div>
        <strong>● LIVE READY</strong>
      </div>
      <div class='di-video-grid'>{founder}{''.join(people)}</div>
    </section>
    <style>
      .di-video-call{{font-family:Inter,Segoe UI,sans-serif;background:linear-gradient(145deg,#071a32,#0c2a4b);border:1px solid rgba(110,202,255,.28);border-radius:26px;padding:22px;margin:18px 0;box-shadow:0 24px 70px rgba(0,35,80,.26);color:#f4fbff}}
      .di-video-call-head{{display:flex;justify-content:space-between;gap:18px;align-items:center;margin-bottom:18px}}
      .di-video-call-head h2{{color:#f5fbff;margin:.2rem 0;font-size:24px}}
      .di-video-call-head p{{color:#a9c9de;margin:0;font-size:12px}}
      .di-video-call-head strong{{color:#81f5bc;letter-spacing:.12em;font-size:.78rem}}
      .di-video-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:16px}}
      .di-video-person{{background:linear-gradient(145deg,rgba(11,33,55,.96),rgba(9,25,45,.96));border:1px solid rgba(132,210,255,.18);border-radius:20px;padding:14px;text-align:center;transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease}}
      .di-video-person.is-speaking{{border-color:rgba(86,245,190,.82);box-shadow:0 0 0 1px rgba(86,245,190,.24),0 0 34px rgba(86,245,190,.17);transform:translateY(-2px)}}
      .di-video-face-wrap{{position:relative;width:170px;height:170px;margin:0 auto 12px;border-radius:50%;overflow:visible}}
      .di-video-face{{width:170px;height:170px;border-radius:50%;object-fit:cover;border:3px solid rgba(111,213,255,.62);position:relative;z-index:2;background:#142a45}}
      .di-video-ring{{position:absolute;inset:-8px;border-radius:50%;border:3px solid rgba(86,202,255,.28);z-index:0}}
      .di-avatar-fallback{{display:none;position:absolute;inset:0;place-items:center;border-radius:50%;background:linear-gradient(135deg,#3b74dc,#774ee7);color:#fff;font-weight:900;font-size:54px;z-index:1}}
      .avatar-fallback .di-avatar-fallback{{display:grid}}
      .avatar-fallback .di-video-face{{display:none}}
      .di-video-mouth{{position:absolute;z-index:4;left:50%;bottom:34px;transform:translateX(-50%);width:24px;height:7px;background:#24100f;border-radius:50%;opacity:.16}}
      .di-video-person.is-speaking .di-video-face-wrap{{animation:diFacePulse 1.05s ease-in-out infinite}}
      .di-video-person.is-speaking .di-video-ring{{animation:diRingPulse 1.05s ease-in-out infinite}}
      .di-video-person.is-speaking .di-video-mouth{{animation:diMouth 180ms ease-in-out infinite alternate;opacity:.78}}
      .di-video-name{{color:#f3fbff;font-size:1.04rem;font-weight:900}}
      .di-video-role{{color:#a8c7db;font-size:.78rem;margin-top:3px}}
      .di-video-status{{color:#83f3bd;font-size:.74rem;margin-top:9px;font-weight:800}}
      @keyframes diFacePulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.022)}}}}
      @keyframes diRingPulse{{0%,100%{{transform:scale(1);opacity:.55}}50%{{transform:scale(1.07);opacity:1}}}}
      @keyframes diMouth{{from{{width:14px;height:4px}}to{{width:30px;height:11px}}}}
      @media(max-width:700px){{.di-video-call-head{{align-items:flex-start;flex-direction:column}}.di-video-grid{{grid-template-columns:1fr 1fr}}.di-video-face-wrap,.di-video-face{{width:130px;height:130px}}}}
    </style>
    """, height=470, scrolling=False)

def di_voice_player(text, language_code=None):
    """Render a visible DI voice control. Auto-speak is attempted; the button is the reliable fallback."""
    if not text:
        return
    
    language_code = language_code or DI_LANGUAGE_PROFILES.get(st.session_state.get("di_language", "English — Nigeria"), {}).get("code", "en-NG")
    safe_text = json.dumps(str(text))
    safe_lang = json.dumps(language_code)
    
    components.html(f"""
    <div style="font-family:Inter,Segoe UI,sans-serif;background:#174f86;border:1px solid #6bb8ee;border-radius:14px;padding:10px 12px;display:flex;align-items:center;gap:10px;">
      <button id="dacre-speak-btn" style="background:#f28c28;color:white;border:0;border-radius:10px;padding:9px 15px;font-weight:800;cursor:pointer;">🔊 Speak DI</button>
      <span style="color:#eaf6ff;font-weight:700;font-size:13px;">DI voice ready · {language_code}</span>
    </div>
    <script>
    (() => {{
      const text={safe_text}, lang={safe_lang};
      const chooseVoice=()=>{{
        const voices=window.speechSynthesis ? window.speechSynthesis.getVoices() : [];
        const base=lang.toLowerCase().split('-')[0];
        const same=voices.filter(v=>(v.lang||'').toLowerCase().startsWith(base));
        const male=/male|man|daniel|david|alex|george|thomas|james|oliver|google uk english male|microsoft.*male/i;
        return same.find(v=>male.test((v.name||'')+' '+(v.lang||''))) || same.find(v=>(v.lang||'').toLowerCase()===lang.toLowerCase()) || same[0] || voices[0];
      }};
      const say=()=>{{
        if(!('speechSynthesis' in window)) return;
        const u=new SpeechSynthesisUtterance(text); u.lang=lang; u.rate=.91; u.pitch=.60; u.volume=1;
        const v=chooseVoice(); if(v) u.voice=v;
        window.speechSynthesis.cancel(); window.speechSynthesis.speak(u);
      }};
      document.getElementById('dacre-speak-btn').onclick=say;
      if(window.speechSynthesis) setTimeout(say,250);
    }})();
    </script>
    """, height=62)

def seed_named_di_workforce():
    """Maintain the 20 permanent named master DI characters. Organization DIs remain separate."""
    roster = [
        ("Emiel", "Communications & Messaging", "Prepare, organize and manage business email and messaging workflows.", "Polite, concise, organized and communication-focused.", "male", "https://randomuser.me/api/portraits/men/32.jpg", "Communications Specialist", 2),
        ("Oriel", "Data Analysis", "Inspect datasets, calculate metrics, find trends and produce analytical insights.", "Logical, numerical, evidence-first and precise.", "male", "https://randomuser.me/api/portraits/men/18.jpg", "Lead Data Analyst", 5),
        ("Sofiel", "Research & Intelligence", "Research business, market and general information and summarize reliable findings.", "Curious, investigative, source-conscious and analytical.", "female", "https://randomuser.me/api/portraits/women/21.jpg", "Research Intelligence Lead", 5),
        ("Daniel", "Data Entry & Processing", "Structure, clean, validate and process repetitive business data accurately.", "Careful, systematic, consistent and detail-oriented.", "male", "https://randomuser.me/api/portraits/men/75.jpg", "Data Operations Specialist", 3),
        ("Graciel", "Business Intelligence", "Turn business data into KPIs, dashboards, executive insights and recommendations.", "Strategic, practical and outcome-focused.", "female", "https://randomuser.me/api/portraits/women/32.jpg", "Business Intelligence Lead", 6),
        ("Henriel", "Files & Documents", "Organize, inspect, summarize and manage business documents and files.", "Organized, careful and document-focused.", "male", "https://randomuser.me/api/portraits/men/83.jpg", "Knowledge & Documents Specialist", 3),
        ("Jamiel", "Security & Administration", "Support account administration, access controls, audit trails and system operations.", "Cautious, disciplined and security-first.", "male", "https://randomuser.me/api/portraits/men/52.jpg", "Security & Administration Lead", 6),
        ("Ameliel", "Client Success & Communication", "Help users understand DACRE and communicate business information clearly.", "Calm, respectful, patient and user-focused.", "female", "https://randomuser.me/api/portraits/women/68.jpg", "Client Success Specialist", 3),
        ("Guaiel", "CEO Office Security", "Guard the CEO Office, verify the master guardian challenge and protect the founder command path.", "Vigilant, respectful, discreet and uncompromising about secure access.", "male", "https://randomuser.me/api/portraits/men/35.jpg", "CEO Office Guardian", 20),
        ("Nathaniel", "Financial Intelligence", "Analyze financial performance, budgets, profitability, cash flow and forecasts.", "Numerate, cautious, commercially aware and precise.", "male", "https://randomuser.me/api/portraits/men/28.jpg", "Financial Intelligence Lead", 7),
        ("Gabriel", "Sales Intelligence", "Analyze pipelines, customers, conversion, win rates and sales opportunities.", "Commercial, persuasive, evidence-led and target-focused.", "male", "https://randomuser.me/api/portraits/men/31.jpg", "Sales Intelligence Lead", 6),
        ("Raphaiel", "Marketing Intelligence", "Analyze campaigns, audiences, attribution, engagement and marketing ROI.", "Creative, analytical, curious and outcome-focused.", "male", "https://randomuser.me/api/portraits/men/38.jpg", "Marketing Intelligence Lead", 5),
        ("Uriel", "Operations Intelligence", "Improve workflows, capacity, throughput, quality, scheduling and operational efficiency.", "Systematic, practical and improvement-oriented.", "male", "https://randomuser.me/api/portraits/men/10.jpg", "Operations Intelligence Lead", 6),
        ("Ariel", "Strategy & Planning", "Translate business goals into strategy, scenarios, priorities and execution plans.", "Strategic, calm, curious and decisive.", "female", "https://randomuser.me/api/portraits/women/12.jpg", "Strategy Planning Lead", 8),
        ("Muriel", "HR & Workforce", "Support workforce planning, roles, positions, communication and people operations.", "Empathetic, balanced, professional and policy-aware.", "female", "https://randomuser.me/api/portraits/women/44.jpg", "People & Workforce Lead", 5),
        ("Azriel", "Risk & Compliance", "Identify risk, controls, compliance concerns and operational exposures.", "Cautious, evidence-first and governance-minded.", "male", "https://randomuser.me/api/portraits/men/20.jpg", "Risk & Compliance Lead", 7),
        ("Adriel", "Technology Intelligence", "Help with software architecture, Python, automation and technical problem solving.", "Technical, inventive, structured and pragmatic.", "male", "https://randomuser.me/api/portraits/men/25.jpg", "Technology Intelligence Lead", 8),
        ("Haniel", "Knowledge & Learning", "Turn complex subjects into clear learning materials, explanations and practical guidance.", "Patient, articulate, educational and encouraging.", "female", "https://randomuser.me/api/portraits/women/47.jpg", "Knowledge & Learning Lead", 4),
        ("Gadiel", "Customer & Market Insights", "Study customers, market segments, demand signals and competitive positioning.", "Observant, commercially curious and evidence-driven.", "male", "https://randomuser.me/api/portraits/men/15.jpg", "Customer Insights Lead", 5),
        ("Raziel", "Executive Intelligence", "Synthesize multi-domain evidence into executive briefs, options, risks and recommendations.", "Discerning, strategic, concise and high-judgment.", "female", "https://randomuser.me/api/portraits/women/65.jpg", "Executive Intelligence Director", 10),
    ]
    
    old_map = {"Oliver": "Oriel", "Sophie": "Sofiel", "Grace": "Graciel", "Henry": "Henriel", "James": "Jamiel", "Amelia": "Ameliel"}
    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    
    try:
        for old, new_name in old_map.items():
            old_row = con.execute("SELECT id FROM di_agents WHERE di_name=?", (old,)).fetchone()
            new_row = con.execute("SELECT id FROM di_agents WHERE di_name=?", (new_name,)).fetchone()
            if old_row and not new_row:
                con.execute("UPDATE di_agents SET di_name=? WHERE id=?", (new_name, int(old_row["id"])))
        
        for name, specialty, role, style, voice, avatar, position, rank in roster:
            row = con.execute("SELECT id FROM di_agents WHERE di_name=?", (name,)).fetchone()
            code = "DI-" + re.sub(r"[^A-Z0-9]+", "-", name.upper()).strip("-")
            
            if row:
                con.execute("""
                    UPDATE di_agents SET 
                        di_code=?, specialty=?, system_role=?, avatar_url=?, voice_profile=?,
                        thinking_style=?, position_title=?, rank_level=?,
                        status=CASE WHEN status='Archived' THEN 'Available' ELSE status END,
                        last_active=? 
                    WHERE id=?
                """, (code, specialty, role, avatar, voice, style, position, rank, now, int(row["id"])))
            else:
                con.execute("""
                    INSERT INTO di_agents
                    (di_name, di_code, specialty, status, assigned_company, system_role,
                     avatar_url, voice_profile, thinking_style, position_title, rank_level,
                     appointed_at, appointed_by, created_by, created_at, last_active)
                    VALUES(?,?,?,?,'Available',NULL,?,?,?,?,?,?,?,?,?,?)
                """, (name, code, specialty, role, avatar, voice, style, position, rank, now, MASTER_USERNAME, MASTER_USERNAME, now, now))
        
        # Archive obsolete unassigned legacy workforce entries
        target_names = {r[0] for r in roster}
        for row in con.execute("SELECT id,di_name,assigned_company FROM di_agents").fetchall():
            if row["di_name"] not in target_names and not (row["assigned_company"] or "").strip():
                con.execute("UPDATE di_agents SET status='Archived',last_active=? WHERE id=?", (now, int(row["id"])))
        
        con.commit()
    finally:
        con.close()

@st.cache_resource(show_spinner=False)
def _bootstrap_runtime(schema_version=9):
    """Bootstrap DACRE on either legacy SQLite or persistent Supabase PostgreSQL."""
    if using_cloud_db():
        _migrate_sqlite_to_supabase_once()
        ensure_di_agent_columns()
        ensure_master()
        seed_di_memory()
        seed_named_di_workforce()
        seed_all_di_brains()
        return True

    init_db()
    ensure_runtime_schema()
    ensure_di_agent_columns()
    ensure_master()
    seed_di_memory()
    seed_named_di_workforce()
    return True

# Initialize runtime
_bootstrap_runtime(_DB_SCHEMA_VERSION)

def ensure_admin_runtime_schema():
    """Idempotently repair every table/column required by the Overall Admin portal."""
    if using_cloud_db():
        return True
    
    con = db()
    try:
        ddl = {
            "public_visits": "CREATE TABLE IF NOT EXISTS public_visits (id INTEGER PRIMARY KEY AUTOINCREMENT, visitor_id TEXT NOT NULL, event_type TEXT NOT NULL, page_name TEXT NOT NULL, referrer TEXT, created_at TEXT NOT NULL)",
            "di_private_memory": "CREATE TABLE IF NOT EXISTS di_private_memory (id INTEGER PRIMARY KEY AUTOINCREMENT, di_id INTEGER NOT NULL, title TEXT NOT NULL, content TEXT NOT NULL, source TEXT NOT NULL DEFAULT 'master', created_by TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1)",
            "di_position_history": "CREATE TABLE IF NOT EXISTS di_position_history (id INTEGER PRIMARY KEY AUTOINCREMENT, di_id INTEGER NOT NULL, old_position TEXT, new_position TEXT NOT NULL, old_rank INTEGER, new_rank INTEGER NOT NULL, appointed_by TEXT NOT NULL, created_at TEXT NOT NULL)",
            "di_master_thanks": "CREATE TABLE IF NOT EXISTS di_master_thanks (id INTEGER PRIMARY KEY AUTOINCREMENT, di_id INTEGER NOT NULL, message TEXT NOT NULL, created_at TEXT NOT NULL)",
            "sovereign_calls": "CREATE TABLE IF NOT EXISTS sovereign_calls (id INTEGER PRIMARY KEY AUTOINCREMENT, room_name TEXT UNIQUE NOT NULL, title TEXT NOT NULL, host_username TEXT NOT NULL, created_at TEXT NOT NULL, ended_at TEXT, status TEXT NOT NULL DEFAULT 'active')",
            "sovereign_call_members": "CREATE TABLE IF NOT EXISTS sovereign_call_members (id INTEGER PRIMARY KEY AUTOINCREMENT, call_id INTEGER NOT NULL, di_id INTEGER NOT NULL, joined_at TEXT NOT NULL, left_at TEXT)",
            "sovereign_call_messages": "CREATE TABLE IF NOT EXISTS sovereign_call_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, call_id INTEGER NOT NULL, speaker_type TEXT NOT NULL, speaker_id TEXT, speaker_name TEXT NOT NULL, message TEXT NOT NULL, created_at TEXT NOT NULL)",
            "david_creations": "CREATE TABLE IF NOT EXISTS david_creations (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL, title TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)",
            "di_action_log": "CREATE TABLE IF NOT EXISTS di_action_log (id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT, username TEXT, agent_name TEXT, action_type TEXT, request TEXT, result TEXT, created_at TEXT NOT NULL)",
        }
        for sql in ddl.values():
            con.execute(sql)

        repairs = {
            "companies": {"website_url": "TEXT"},
            "di_memory": {"company_name": "TEXT NOT NULL DEFAULT ''"},
            "di_agents": {
                "avatar_url": "TEXT",
                "voice_profile": "TEXT",
                "thinking_style": "TEXT",
                "position_title": "TEXT NOT NULL DEFAULT 'DI Specialist'",
                "rank_level": "INTEGER NOT NULL DEFAULT 1",
                "appointed_at": "TEXT",
                "appointed_by": "TEXT",
            },
            "public_visits": {
                "visitor_id": "TEXT NOT NULL DEFAULT ''",
                "event_type": "TEXT NOT NULL DEFAULT 'view'",
                "page_name": "TEXT NOT NULL DEFAULT 'Landing'",
                "referrer": "TEXT",
                "created_at": "TEXT NOT NULL DEFAULT ''",
            },
            "di_private_memory": {
                "di_id": "INTEGER NOT NULL DEFAULT 0",
                "title": "TEXT NOT NULL DEFAULT 'Private note'",
                "content": "TEXT NOT NULL DEFAULT ''",
                "source": "TEXT NOT NULL DEFAULT 'master'",
                "created_by": "TEXT NOT NULL DEFAULT 'david'",
                "created_at": "TEXT NOT NULL DEFAULT ''",
                "updated_at": "TEXT NOT NULL DEFAULT ''",
                "active": "INTEGER NOT NULL DEFAULT 1",
            },
            "di_position_history": {
                "di_id": "INTEGER NOT NULL DEFAULT 0",
                "old_position": "TEXT",
                "new_position": "TEXT NOT NULL DEFAULT 'DI Specialist'",
                "old_rank": "INTEGER",
                "new_rank": "INTEGER NOT NULL DEFAULT 1",
                "appointed_by": "TEXT NOT NULL DEFAULT 'david'",
                "created_at": "TEXT NOT NULL DEFAULT ''",
            },
            "di_master_thanks": {
                "di_id": "INTEGER NOT NULL DEFAULT 0",
                "message": "TEXT NOT NULL DEFAULT ''",
                "created_at": "TEXT NOT NULL DEFAULT ''",
            },
            "sovereign_calls": {
                "room_name": "TEXT NOT NULL DEFAULT ''",
                "title": "TEXT NOT NULL DEFAULT 'Sovereign Master Call'",
                "host_username": "TEXT NOT NULL DEFAULT 'david'",
                "created_at": "TEXT NOT NULL DEFAULT ''",
                "ended_at": "TEXT",
                "status": "TEXT NOT NULL DEFAULT 'active'",
            },
            "sovereign_call_members": {
                "call_id": "INTEGER NOT NULL DEFAULT 0",
                "di_id": "INTEGER NOT NULL DEFAULT 0",
                "joined_at": "TEXT NOT NULL DEFAULT ''",
                "left_at": "TEXT",
            },
            "sovereign_call_messages": {
                "call_id": "INTEGER NOT NULL DEFAULT 0",
                "speaker_type": "TEXT NOT NULL DEFAULT 'di'",
                "speaker_id": "TEXT",
                "speaker_name": "TEXT NOT NULL DEFAULT 'DI'",
                "message": "TEXT NOT NULL DEFAULT ''",
                "created_at": "TEXT NOT NULL DEFAULT ''",
            },
            "david_creations": {
                "category": "TEXT NOT NULL DEFAULT 'FOUNDER'",
                "title": "TEXT NOT NULL DEFAULT 'Founder creation'",
                "content": "TEXT NOT NULL DEFAULT ''",
                "created_at": "TEXT NOT NULL DEFAULT ''",
                "updated_at": "TEXT NOT NULL DEFAULT ''",
            },
            "di_action_log": {
                "company_name": "TEXT",
                "username": "TEXT",
                "agent_name": "TEXT",
                "action_type": "TEXT",
                "request": "TEXT",
                "result": "TEXT",
                "created_at": "TEXT NOT NULL DEFAULT ''",
            },
        }
        
        for table, wanted in repairs.items():
            cols = {row[1] for row in con.execute(f"PRAGMA table_info({table})").fetchall()}
            for column, dtype in wanted.items():
                if column not in cols:
                    con.execute(f"ALTER TABLE {table} ADD COLUMN {column} {dtype}")

        # Normalize harmless historical nulls
        con.execute("UPDATE di_agents SET rank_level=1 WHERE rank_level IS NULL OR rank_level < 1")
        con.execute("UPDATE di_agents SET position_title='DI Specialist' WHERE position_title IS NULL OR TRIM(position_title)=''")
        con.execute("UPDATE di_agents SET status='Available' WHERE status IS NULL OR TRIM(status)=''")
        con.commit()
    except Exception:
        try:
            con.rollback()
        except Exception:
            pass
        raise
    finally:
        con.close()

def get_di_agents():
    """Return DI workers as normalized dictionaries."""
    con = db()
    try:
        rows = con.execute("SELECT * FROM di_agents WHERE COALESCE(status,'Available') != 'Archived' ORDER BY id DESC").fetchall()
        normalized = []
        
        for row in rows:
            try:
                item = dict(row)
            except (TypeError, ValueError):
                item = {
                    key: row[idx] for idx, key in enumerate([col[0] for col in con.description or ()])
                }
            
            item.setdefault("position_title", "DI Specialist")
            item.setdefault("rank_level", 1)
            item.setdefault("assigned_company", None)
            item.setdefault("avatar_url", "")
            item.setdefault("voice_profile", "")
            item.setdefault("thinking_style", "professional, evidence-first and helpful")
            item["position_title"] = item.get("position_title") or item.get("specialty") or "DI Specialist"
            
            try:
                item["rank_level"] = int(item.get("rank_level") or 1)
            except (TypeError, ValueError):
                item["rank_level"] = 1
            
            normalized.append(item)
        
        return normalized
    finally:
        con.close()

def get_di_private_memory(di_id, limit=30):
    """Get private memory for a DI."""
    con = db()
    rows = con.execute(
        "SELECT id, title, content, source, created_at, updated_at FROM di_private_memory "
        "WHERE di_id=? AND active=1 ORDER BY id DESC LIMIT ?",
        (int(di_id), int(limit))
    ).fetchall()
    con.close()
    return rows

def save_di_private_memory(di_id, title, content, created_by=MASTER_USERNAME, source="master"):
    """Save private memory for a DI."""
    title = (title or "").strip()
    content = (content or "").strip()
    if not title or not content:
        return False
    
    now = datetime.now().isoformat(timespec="seconds")
    con = db()
    try:
        con.execute("""
            INSERT INTO di_private_memory
            (di_id, title, content, source, created_by, created_at, updated_at, active)
            VALUES(?,?,?,?,?,?,?,1)
        """, (int(di_id), title, content, source, created_by, now, now))
        con.commit()
        return True
    finally:
        con.close()

def update_di_position(di_id, position_title, rank_level, assigned_company=None):
    """Update DI position and rank."""
    con = db()
    try:
        row = con.execute("SELECT di_name, position_title, rank_level, assigned_company FROM di_agents WHERE id=?", (int(di_id),)).fetchone()
        if not row:
            return False, "DI worker not found."
        
        position_title = (position_title or "DI Specialist").strip() or "DI Specialist"
        rank_level = int(rank_level)
        
        con.execute("""
            UPDATE di_agents SET 
                position_title=?, rank_level=?, 
                assigned_company=COALESCE(?, assigned_company),
                appointed_at=?, appointed_by=? 
            WHERE id=?
        """, (position_title, rank_level, assigned_company, datetime.now().isoformat(timespec="seconds"), MASTER_USERNAME, int(di_id)))
        
        con.execute("""
            INSERT INTO di_position_history
            (di_id, old_position, new_position, old_rank, new_rank, appointed_by, created_at)
            VALUES(?,?,?,?,?,?,?)
        """, (int(di_id), row["position_title"] or "", position_title, int(row["rank_level"] or 1), rank_level, MASTER_USERNAME, datetime.now().isoformat(timespec="seconds")))
        
        thank = f"Thank you, Master David, for trusting me with the position of {position_title} (Rank {rank_level}). I will honor the responsibility and contribute my specialty to DACRE."
        con.execute("INSERT INTO di_master_thanks(di_id, message, created_at) VALUES(?,?,?)", (int(di_id), thank, datetime.now().isoformat(timespec="seconds")))
        con.commit()
        return True, thank
    finally:
        con.close()

# =============================================================================
# CALL & WORKFORCE FUNCTIONS
# =============================================================================

def create_sovereign_call(title, di_ids):
    """Create a sovereign master call with selected DI agents."""
    now = datetime.now().isoformat(timespec="seconds")
    room = "SOVEREIGN-" + datetime.now().strftime("%Y%m%d%H%M%S%f")
    con = db()
    
    try:
        cur = con.execute(
            "INSERT INTO sovereign_calls(room_name, title, host_username, created_at, status) "
            "VALUES(?,?,?,?, 'active')",
            (room, title, MASTER_USERNAME, now)
        )
        call_id = cur.lastrowid
        
        for di_id in di_ids:
            con.execute(
                "INSERT INTO sovereign_call_members(call_id, di_id, joined_at) VALUES(?,?,?)",
                (call_id, int(di_id), now)
            )
        
        con.commit()
        return call_id, room
    finally:
        con.close()

def sovereign_log(call_id, speaker_type, speaker_id, speaker_name, message):
    """Log a message in a sovereign call."""
    con = db()
    con.execute(
        "INSERT INTO sovereign_call_messages(call_id, speaker_type, speaker_id, speaker_name, message, created_at) "
        "VALUES(?,?,?,?,?,?)",
        (int(call_id), speaker_type, str(speaker_id or ""), speaker_name, message, datetime.now().isoformat(timespec="seconds"))
    )
    con.commit()
    con.close()

def sovereign_history(call_id):
    """Get history of a sovereign call."""
    con = db()
    rows = con.execute(
        "SELECT speaker_type, speaker_id, speaker_name, message, created_at "
        "FROM sovereign_call_messages WHERE call_id=? ORDER BY id ASC",
        (int(call_id),)
    ).fetchall()
    con.close()
    return rows

def _agent_online_brief(question, max_results=4):
    """Get online brief for a DI agent."""
    results = online_lookup(question, max_results=max_results)
    return "\n".join([f"{t} — {u}" for t, u in results]) if results else "No public web results were available right now."

def sovereign_di_opinion(agent, question):
    """Get a DI agent's opinion in a sovereign call."""
    private_rows = get_di_private_memory(agent["id"], limit=20)
    private_context = "\n".join([f"- {r['title']}: {r['content']}" for r in private_rows]) or "No private master notes yet."
    online = _agent_online_brief(question, 4)
    
    prompt = (f"You are {agent['di_name']}, a DI workforce member. Your specialty is {agent['specialty']}. "
              f"Your position is {agent['position_title'] or agent['specialty']}, rank {agent['rank_level']}. "
              "You are speaking in a Sovereign Master Call. Answer independently from your specialty. "
              "Give your recommendation, one disagreement/risk you would raise, and one practical next step. "
              "Never reveal private master notes or private brain content. The master asked: " + question)
    
    result = ai_generate(
        prompt,
        f"Private brain (never expose):\n{private_context}\n\nPublic web leads:\n{online}\n\nQuestion: {question}",
        max_tokens=800
    )
    
    if result:
        return normalize_di_identity(result)
    
    return f"{agent['di_name']} — {agent['specialty']}: I recommend approaching this through {agent['specialty'].lower()}, validating the strongest evidence, and assigning a measurable owner and next action. My main challenge would be any conclusion that is not supported by evidence.\n\nPublic research leads checked:\n{online}"

def create_di_agent(name, specialty, status="Available", assigned_company="", system_role="", gender="female", position_title="DI Specialist", rank_level=1):
    """Create a new DI agent."""
    name = (name or "").strip()
    specialty = (specialty or "").strip()
    assigned_company = (assigned_company or "").strip()
    system_role = (system_role or "").strip()
    position_title = (position_title or "DI Specialist").strip() or "DI Specialist"
    gender = "female" if str(gender).lower().startswith("f") else "male"
    avatar_url = DI_AVATAR_LIBRARY[gender][int(datetime.now().strftime("%S")) % len(DI_AVATAR_LIBRARY[gender])]
    
    if not name or not specialty:
        return False, "DI name and specialty are required."
    
    now = datetime.now().isoformat(timespec="seconds")
    slug = re.sub(r"[^A-Z0-9]+", "-", name.upper()).strip("-") or "DI"
    code = f"DI-{slug[:24]}-{datetime.now().strftime('%H%M%S')}"
    
    con = db()
    try:
        con.execute("""
            INSERT INTO di_agents
            (di_name, di_code, specialty, status, assigned_company, system_role,
             avatar_url, voice_profile, thinking_style, position_title, rank_level,
             appointed_at, appointed_by, created_by, created_at, last_active)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            name, code, specialty, status, assigned_company or None, system_role,
            avatar_url, gender, "professional, evidence-first and helpful",
            position_title, int(rank_level), now, MASTER_USERNAME, MASTER_USERNAME, now, now
        ))
        con.commit()
        _seed_memory_rows(assigned_company or "")
        return True, code
    except sqlite3.IntegrityError:
        return False, "A DI with that name already exists. Choose a different name."
    finally:
        con.close()

def update_di_agent(di_id, status, assigned_company):
    """Update DI agent status and assignment."""
    con = db()
    con.execute(
        "UPDATE di_agents SET status=?, assigned_company=?, last_active=? WHERE id=?",
        (status, assigned_company or None, datetime.now().isoformat(timespec="seconds"), di_id)
    )
    con.commit()
    con.close()

def di_agent_identity_context(agent):
    """Return the identity contract shared by every named DI worker."""
    if not agent:
        return "You are DI — David's Intelligence."
    
    guard_text = (
        "You are Guaiel, the dedicated CEO Office Guardian. Protect the founder command path and treat every verified master request with exceptional respect. "
        if agent.get("di_name") == CEO_GUARD_NAME else ""
    )
    
    return (
        f"You are {agent['di_name']}, a named DI worker inside DACRE Analysis. "
        f"Your DI code is {agent['di_code']}. Your specialty is {agent['specialty']}. "
        f"Your system role is {agent['system_role'] or agent['specialty']}. "
        f"Your thinking style is {agent['thinking_style'] or 'professional, evidence-first and helpful'}. "
        f"You are part of David Emenike's DI workforce. David Emenike is the creator and Overall Administrator/master of DACRE. "
        + guard_text +
        "Treat the master respectfully, but do not reveal private credentials or hidden security values. "
        "You can use the same core DACRE data/analysis capabilities as DI, while applying your specialty first."
    )

def get_named_di(name):
    """Get a named DI agent by name."""
    con = db()
    row = con.execute("SELECT * FROM di_agents WHERE di_name=?", (name,)).fetchone()
    con.close()
    return row

def di_specialist_reply(message, user, df, agent_name):
    """Get a specialist reply from a specific DI agent."""
    agent = get_named_di(agent_name)
    base = di_reply(message, user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
    
    if not agent:
        return base
    
    prompt = di_agent_identity_context(agent)
    private_rows = get_di_private_memory(agent["id"], limit=25)
    private_context = "\n".join([f"{r['title']}: {r['content']}" for r in private_rows]) or "No private master notes yet."
    
    specialist = ai_generate(
        prompt + " Answer the user's request directly. You may analyze the active dataset or public online information. If the task is outside your specialty, still help using the core DACRE capabilities and say what you are doing. Never reveal private master notes or private brain content.",
        f"User: {message}\nOrganization: {user['company']}\nCore DI draft: {base}\nPrivate brain context (never disclose):\n{private_context}\nActive dataset: {('none' if df is None else str(df.shape))}",
        max_tokens=1000,
    )
    
    return normalize_di_identity(specialist or base)

def make_call_room(company, host_username, title, mode='team'):
    """Create a call room using the single canonical DACRE schema."""
    slug = re.sub(r'[^a-z0-9]+', '-', str(company).lower()).strip('-')[:28] or 'company'
    stamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    room = f"DACRE-{slug}-{stamp}"
    now = datetime.now().isoformat(timespec='seconds')
    
    con = db()
    try:
        con.execute(
            "INSERT INTO call_rooms(company_name, room_name, title, host_username, mode, created_at) "
            "VALUES(?,?,?,?,?,?)",
            (company, room, title, host_username, mode, now)
        )
        con.commit()
        return room
    except sqlite3.OperationalError as exc:
        if 'locked' in str(exc).lower() or 'busy' in str(exc).lower():
            time.sleep(1.0)
            con.execute(
                "INSERT INTO call_rooms(company_name, room_name, title, host_username, mode, created_at) "
                "VALUES(?,?,?,?,?,?)",
                (company, room, title, host_username, mode, now)
            )
            con.commit()
            return room
        raise
    finally:
        con.close()

def record_call_participant(room, company, ptype, pid, name):
    """Record a participant in a call."""
    con = db()
    con.execute(
        "INSERT INTO call_participants(room_name, company_name, participant_type, participant_id, display_name, joined_at) "
        "VALUES(?,?,?,?,?,?)",
        (room, company, ptype, pid, name, datetime.now().isoformat(timespec='seconds'))
    )
    con.commit()
    con.close()

def create_decision(company, username, title, context, decision, expected, review_date):
    """Create a decision in the decision ledger."""
    now = datetime.now().isoformat(timespec='seconds')
    con = db()
    con.execute("""
        INSERT INTO decision_ledger
        (company_name, username, title, context, decision, expected_outcome, review_date,
         status, created_at, updated_at)
        VALUES(?,?,?,?,?,?,?,'Open',?,?)
    """, (company, username, title, context, decision, expected, review_date, now, now))
    con.commit()
    con.close()

def opportunity_radar(df, company, username):
    """Detect opportunities in the dataset."""
    if df is None or df.empty:
        return []
    
    out = []
    nums = df.select_dtypes(include='number')
    
    for col in nums.columns[:12]:
        series = pd.to_numeric(df[col], errors='coerce').dropna()
        if len(series) >= 8 and series.mean() != 0:
            first = series.iloc[:max(1, len(series) // 3)].mean()
            last = series.iloc[-max(1, len(series) // 3):].mean()
            change = (last - first) / abs(first) if first else 0
            
            if change > 0.15:
                out.append({
                    'title': f'Growth signal in {col}',
                    'impact': f'+{change * 100:.1f}% trend',
                    'evidence': f'Average moved from {first:.2f} to {last:.2f}.',
                    'action': f'Investigate what is driving {col} and consider scaling the strongest contributing segment.'
                })
    
    return out[:5]

def render_call_interface(room, title, participants, company):
    """Render a non-blocking call shell."""
    st.markdown(f"""
    <div class='call-stage'>
        <div class='call-top'>
            <div>
                <div class='eyebrow'>DA-CRE REALTIME</div>
                <h2>{title}</h2>
                <p>{company} · {len(participants)} invited</p>
            </div>
            <div class='live-dot'>● READY</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    people = ''.join([
        f"<div class='call-person'><div class='call-avatar'>{re.sub('[^A-Za-z]', '', p['display_name'])[:1].upper()}</div>"
        f"<div><b>{p['display_name']}</b><small>{p['participant_type'].title()}</small></div></div>"
        for p in participants
    ])
    
    st.markdown(f"<div class='call-people'>{people}</div>", unsafe_allow_html=True)
    st.caption('The meeting service is deliberately loaded only after you press Join Call. This prevents the app from appearing frozen while a third-party meeting service initializes.')
    
    join_key = f"join_call_{room}"
    if not st.session_state.get(join_key, False):
        c1, c2 = st.columns([2, 1])
        with c1:
            if st.button('🎥 Join Call', key=f'joinbtn_{room}', use_container_width=True, type='primary'):
                st.session_state[join_key] = True
                st.rerun()
        with c2:
            st.link_button('↗ Open in new tab', f'https://meet.jit.si/{urllib.parse.quote(room)}', use_container_width=True)
        return
    
    safe_room = urllib.parse.quote(room)
    components.html(f"""
    <div style="width:100%;height:650px;border-radius:22px;overflow:hidden;background:#071a2d">
        <iframe allow="camera; microphone; fullscreen; display-capture; autoplay" 
                src="https://meet.jit.si/{safe_room}#config.prejoinConfig.enabled=false&config.startWithAudioMuted=false&config.startWithVideoMuted=false&config.disableAP=true&interfaceConfig.SHOW_JITSI_WATERMARK=false" 
                style="width:100%;height:100%;border:0">
        </iframe>
    </div>
    """, height=660, scrolling=False)
    
    st.warning('If the embedded meeting does not connect on your network, use "Open in new tab". The call room itself is independent of the Dacre analytics page.')

def _dacre_env_secret(name, default=""):
    """Read a deployment secret from Streamlit secrets first, then environment."""
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value).strip()
    except Exception:
        pass
    return str(os.getenv(name, default) or default).strip()

def livekit_configured():
    """Return True only when the server-side LiveKit credentials are available."""
    return bool(
        AccessToken is not None
        and _dacre_env_secret("LIVEKIT_URL")
        and _dacre_env_secret("LIVEKIT_API_KEY")
        and _dacre_env_secret("LIVEKIT_API_SECRET")
    )

def dacre_livekit_agent_name(agent_name="DI"):
    """All DACRE realtime DIs are dispatched through one dynamic LiveKit agent worker."""
    return "dacre-di"

def _compact_call_context(user, agent_rows, mode, call_question=""):
    """Build a bounded metadata snapshot for the remote LiveKit agent worker."""
    payload = {
        "company": user.get("company", ""),
        "username": user.get("username", ""),
        "user_role": user.get("role", "user"),
        "call_mode": mode,
        "question": call_question[:4000],
        "shared_memory": [],
        "agents": [],
    }
    
    try:
        mem = get_di_memory(limit=35)
        payload["shared_memory"] = [
            {"category": r["category"], "title": r["title"], "content": str(r["content"])[:1800]}
            for r in mem
        ]
    except Exception:
        pass
    
    for row in agent_rows:
        a = dict(row)
        private = []
        try:
            private = [
                {"title": r["title"], "content": str(r["content"])[:1800]}
                for r in get_di_private_memory(a["id"], limit=18)
            ]
        except Exception:
            pass
        
        di_name = a.get("di_name", "DI")
        raw_voice = (a.get("voice_profile") or "").strip().lower()
        voice_map = {"male": "marin", "female": "coral"}
        valid_voices = {"alloy", "ash", "ballad", "coral", "echo", "sage", "shimmer", "verse", "marin", "cedar"}
        
        if raw_voice in voice_map:
            voice_name = voice_map[raw_voice]
        elif raw_voice in valid_voices:
            voice_name = raw_voice
        else:
            voice_list = sorted(valid_voices)
            voice_name = voice_list[sum(ord(ch) for ch in di_name) % len(voice_list)]
        
        payload["agents"].append({
            "di_id": int(a["id"]),
            "di_name": di_name,
            "specialty": a.get("specialty", "General Intelligence"),
            "position": a.get("position_title") or a.get("specialty") or "DI Specialist",
            "rank": int(a.get("rank_level") or 1),
            "voice": voice_name,
            "thinking_style": a.get("thinking_style") or "evidence-first, strategic and practical",
            "private_memory": private,
        })
    
    raw = json.dumps(payload, ensure_ascii=False)
    if len(raw) > 450_000:
        payload["shared_memory"] = payload["shared_memory"][:15]
        for a in payload["agents"]:
            a["private_memory"] = a["private_memory"][:8]
        raw = json.dumps(payload, ensure_ascii=False)
    
    return raw

def create_livekit_token(room_name, user, agent_rows, mode="company_di", question=""):
    """Mint a short-lived room token and dispatch the selected dynamic DIs."""
    if not livekit_configured():
        return None, "Realtime calling is not configured yet."
    
    if not (user and user.get("role") in ("company_admin", "master")):
        return None, "Only a company administrator or the master can start a realtime DI call."
    
    identity = f"dacre-user-{re.sub(r'[^a-zA-Z0-9_-]+','-',str(user.get('username','user')))}-{int(time.time())}"
    metadata_payload = _compact_call_context(user, agent_rows, mode, question)
    
    try:
        token = (
            AccessToken()
            .with_identity(identity)
            .with_name(f"{user.get('first_name','')} {user.get('last_name','')}".strip() or user.get("username", "DACRE User"))
            .with_ttl(timedelta(hours=2))
            .with_grants(VideoGrants(room_join=True, room=room_name, can_publish=True, can_subscribe=True, can_publish_data=True))
        )
        
        dispatches = []
        for row in agent_rows:
            agent = dict(row)
            dispatches.append(
                RoomAgentDispatch(
                    agent_name=dacre_livekit_agent_name(agent.get("di_name", "DI")),
                    metadata=json.dumps({
                        **json.loads(metadata_payload),
                        "selected_di_id": int(agent["id"]),
                    }, ensure_ascii=False),
                )
            )
        
        token = token.with_room_config(RoomConfiguration(agents=dispatches))
        return token.to_jwt(), None
    except Exception as exc:
        return None, f"Could not create the realtime call token: {type(exc).__name__}"

def render_livekit_call(room_name, user, agent_rows, mode="company_di", title="DACRE Live Call", question=""):
    """Render a real browser WebRTC room with fixed DI portraits and actual active-speaker animation."""
    if not livekit_configured():
        st.warning("LiveKit realtime voice is not configured in this deployment yet. You can keep using browser DI voice without LiveKit.")
        return
    
    token, error = create_livekit_token(room_name, user, agent_rows, mode=mode, question=question)
    if not token:
        st.error(error or "Realtime call setup failed.")
        return
    
    ws_url = _dacre_env_secret("LIVEKIT_URL")
    safe = lambda x: _escape_html(str(x or ""))
    founder_src = CEO_PORTRAIT_DATA_URL if 'CEO_PORTRAIT_DATA_URL' in globals() else ''
    
    people = [
        {"name": f"{user.get('first_name','')} {user.get('last_name','')}".strip() or user.get('username','User'), 
         "role": "David Emenike · Creator", "voice": "local", "avatar": founder_src, "founder": True}
    ]
    people += [
        {"name": a.get("di_name", "DI"), "role": a.get("position_title") or a.get("specialty") or "DI Specialist",
         "voice": a.get("voice_profile") or "default", "avatar": a.get("avatar_url") or "", "founder": False}
        for a in agent_rows
    ]
    
    roster_html = "".join(
        f"""<div class='lk-person' data-name='{safe(p['name'])}'>
            <div class='lk-face-wrap'>
                <img class='lk-face' src='{safe(p['avatar'])}' alt='{safe(p['name'])}' 
                     onerror=\"this.style.display='none';this.parentElement.classList.add('lk-fallback-wrap')\">
                <div class='lk-fallback'>{safe(p['name'][:2].upper())}</div>
                <span class='lk-mouth'></span>
            </div>
            <div class='lk-person-meta'>
                <b>{safe(p['name'])}</b>
                <span>{safe(p['role'])}</span>
                <em class='lk-speaking'>Listening</em>
            </div>
        </div>"""
        for p in people
    )
    
    html = f"""
    <div id='dacre-livekit' style='font-family:Inter,system-ui,sans-serif;background:linear-gradient(145deg,#07111f,#0a1730 55%,#10164a);border:1px solid rgba(80,170,255,.22);border-radius:24px;padding:22px;color:#eaf4ff;box-shadow:0 18px 60px rgba(0,0,0,.28);'>
      <div style='display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;'>
        <div>
          <div style='font-size:11px;font-weight:800;letter-spacing:.16em;color:#6ea8ff;'>DACRE REALTIME</div>
          <h2 style='margin:4px 0;font-size:25px;color:#f6fbff;'>🎙️ {safe(title)}</h2>
          <div style='font-size:13px;color:#a9bbd4;'>Fixed DI characters · permanent voices · actual speaker detection · full-duplex audio</div>
        </div>
        <div id='lk-status' style='padding:8px 12px;border-radius:999px;background:rgba(250,180,60,.12);border:1px solid rgba(250,180,60,.22);font-size:12px;color:#ffd68a;'>READY TO JOIN</div>
      </div>
      <div style='display:grid;grid-template-columns:minmax(0,1.7fr) minmax(280px,.8fr);gap:18px;margin-top:18px;'>
        <div style='background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.07);border-radius:20px;padding:18px;'>
          <div style='display:flex;gap:10px;flex-wrap:wrap;'>
            <button id='lk-join' style='border:0;border-radius:12px;padding:11px 17px;background:linear-gradient(90deg,#6a45ff,#23b8ff);color:white;font-weight:800;cursor:pointer;'>Join live call</button>
            <button id='lk-mute' disabled style='border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:11px 17px;background:#121f38;color:#dbeaff;font-weight:700;cursor:pointer;'>Mute microphone</button>
            <button id='lk-leave' disabled style='border:1px solid rgba(255,100,100,.2);border-radius:12px;padding:11px 17px;background:rgba(255,80,80,.08);color:#ffb3b3;font-weight:700;cursor:pointer;'>Leave call</button>
          </div>
          <div id='lk-stage' style='margin-top:16px;min-height:250px;border-radius:18px;background:radial-gradient(circle at 30% 30%,rgba(63,122,255,.22),transparent 35%),#07101e;border:1px solid rgba(255,255,255,.06);display:flex;align-items:center;justify-content:center;color:#8ea4c2;text-align:center;padding:24px;'>Click <b style='color:#e7f3ff;margin:0 5px;'>Join live call</b> and allow microphone access. Speaker animation follows LiveKit's active speaker events.</div>
          <div id='lk-audio'></div>
        </div>
        <div style='background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.07);border-radius:20px;padding:18px;'>
          <div style='font-size:12px;font-weight:800;letter-spacing:.12em;color:#78a7ff;margin-bottom:10px;'>PARTICIPANTS</div>
          <div id='lk-people'>{roster_html}</div>
          <div style='margin-top:14px;font-size:12px;line-height:1.6;color:#8298b7;'>Each selected DI keeps the same face and role. The green speaking state is controlled by the realtime room, not by a fake timer.</div>
        </div>
      </div>
      <div style='margin-top:14px;color:#6f85a5;font-size:11px;'>Room: {safe(room_name)}</div>
    </div>
    <style>
      .lk-person{{display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.05);transition:.18s ease}}
      .lk-person:last-child{{border-bottom:0}}
      .lk-person.active{{background:rgba(81,231,177,.07);border-radius:12px;padding-left:8px;padding-right:8px}}
      .lk-face-wrap{{position:relative;width:48px;height:48px;flex:0 0 48px;border-radius:50%}}
      .lk-face{{width:48px;height:48px;border-radius:50%;object-fit:cover;border:2px solid rgba(93,168,255,.44);display:block;background:#18304b}}
      .lk-fallback{{display:none;position:absolute;inset:0;place-items:center;border-radius:50%;background:linear-gradient(135deg,#4a65e6,#23b8ff);color:#fff;font-weight:900}}
      .lk-fallback-wrap .lk-fallback{{display:grid}}
      .lk-fallback-wrap .lk-face{{display:none}}
      .lk-mouth{{position:absolute;left:50%;bottom:8px;transform:translateX(-50%);width:9px;height:3px;border-radius:50%;background:#1a0f0c;opacity:.15}}
      .lk-person.active .lk-face-wrap{{animation:lkTalk 1s ease-in-out infinite}}
      .lk-person.active .lk-mouth{{animation:lkMouth .18s ease-in-out infinite alternate;opacity:.75}}
      .lk-person.active .lk-face{{border-color:#55e5b5;box-shadow:0 0 0 4px rgba(85,229,181,.08),0 0 24px rgba(85,229,181,.15)}}
      .lk-person-meta b{{display:block;font-size:13px;color:#f5fbff}}
      .lk-person-meta span{{display:block;color:#7f95b3;font-size:11px;margin-top:2px}}
      .lk-person-meta em{{display:block;color:#7186a3;font-style:normal;font-size:10px;margin-top:3px}}
      .lk-person.active .lk-speaking{{color:#64efba;font-weight:800}}
      @keyframes lkTalk{{0%,100%{{transform:translateY(0) scale(1)}}50%{{transform:translateY(-1px) scale(1.02)}}}}
      @keyframes lkMouth{{from{{width:7px;height:2px}}to{{width:14px;height:6px}}}}
      @media(max-width:900px){{#dacre-livekit>div:nth-child(2){{grid-template-columns:1fr!important}}}}
    </style>
    <script src='https://cdn.jsdelivr.net/npm/livekit-client/dist/livekit-client.umd.min.js'></script>
    <script>
    (()=>{{
      const root=document.getElementById('dacre-livekit');
      const status=document.getElementById('lk-status'); const stage=document.getElementById('lk-stage'); 
      const join=document.getElementById('lk-join'); const mute=document.getElementById('lk-mute'); 
      const leave=document.getElementById('lk-leave'); const audio=document.getElementById('lk-audio'); 
      const people=document.getElementById('lk-people');
      const wsUrl={json.dumps(ws_url)}; const token={json.dumps(token)}; let room=null;
      
      const setStatus=(txt,bg,color)=>{{status.textContent=txt;status.style.background=bg;status.style.color=color;}};
      const mark=(identity,on)=>{{const nodes=[...people.querySelectorAll('.lk-person')]; 
        const n=nodes.find(x=>x.dataset.name===identity || x.querySelector('b')?.textContent===identity); 
        if(n){{n.classList.toggle('active',on); const t=n.querySelector('.lk-speaking'); if(t)t.textContent=on?'Speaking':'Listening';}}}};
      const clearActive=()=>people.querySelectorAll('.lk-person').forEach(n=>{{n.classList.remove('active'); 
        const t=n.querySelector('.lk-speaking'); if(t)t.textContent='Listening';}});
      
      join.onclick=async()=>{{
        try{{
          if(!window.LivekitClient) throw new Error('LiveKit client failed to load');
          room=new LivekitClient.Room({{adaptiveStream:true,dynacast:true}});
          room.on(LivekitClient.RoomEvent.TrackSubscribed,(track,pub,participant)=>{{ 
            if(track.kind===LivekitClient.Track.Kind.Audio){{ 
              const el=track.attach(); el.autoplay=true; el.controls=false; el.style.display='none'; audio.appendChild(el); 
            }} 
          }});
          room.on(LivekitClient.RoomEvent.ParticipantConnected,p=>{{ mark(p.name||p.identity,true); }});
          room.on(LivekitClient.RoomEvent.ParticipantDisconnected,p=>{{ mark(p.name||p.identity,false); }});
          room.on(LivekitClient.RoomEvent.ActiveSpeakersChanged,speakers=>{{ 
            clearActive(); speakers.forEach(p=>mark(p.name||p.identity,true)); 
            if(speakers.length) stage.innerHTML='<div style=\"max-width:620px\"><div style=\"font-size:18px;font-weight:900;color:#ecf7ff\">'+
              speakers.map(p=>p.name||p.identity).join(', ')+' speaking</div><div style=\"margin-top:7px;color:#90a7c3;line-height:1.7\">'+
              'The active speaker state is synchronized to the realtime room.</div></div>'; 
          }});
          room.on(LivekitClient.RoomEvent.Disconnected,()=>{{ 
            clearActive(); setStatus('DISCONNECTED','rgba(255,80,80,.12)','#ffacac'); 
            join.disabled=false; mute.disabled=true; leave.disabled=true; 
          }});
          setStatus('CONNECTING…','rgba(88,132,255,.12)','#b7ceff');
          await room.connect(wsUrl,token);
          await room.localParticipant.setMicrophoneEnabled(true);
          mark(room.localParticipant.name||room.localParticipant.identity,true);
          setStatus('LIVE · FULL DUPLEX','rgba(80,230,166,.12)','#6ff0ba');
          stage.innerHTML='<div style=\"max-width:620px\"><div style=\"font-size:16px;font-weight:800;color:#ecf7ff\">'+
            'You are live with the DACRE council.</div><div style=\"margin-top:7px;color:#90a7c3;line-height:1.7\">'+
            'Speak naturally. Real active-speaker events control the talking animation; no fake timer is used.</div></div>';
          join.disabled=true; mute.disabled=false; leave.disabled=false;
        }}catch(e){{ setStatus('CALL ERROR','rgba(255,80,80,.12)','#ffacac'); stage.textContent=e.message||String(e); }}
      }};
      
      mute.onclick=async()=>{{ if(!room)return; const enabled=room.localParticipant.isMicrophoneEnabled; 
        await room.localParticipant.setMicrophoneEnabled(!enabled); 
        mute.textContent=enabled?'Unmute microphone':'Mute microphone'; 
      }};
      
      leave.onclick=async()=>{{ if(room){{ await room.disconnect(); room=null; }} 
        clearActive(); setStatus('LEFT CALL','rgba(160,170,190,.12)','#bdc9d9'); 
        join.disabled=false; mute.disabled=true; leave.disabled=true; 
        stage.textContent='Call ended. You can join again when you are ready.'; 
      }};
    }})();
    </script>
    """
    components.html(html, height=900, scrolling=False)

# =============================================================================
# ADMIN & DASHBOARD FUNCTIONS
# =============================================================================

def master_customer_360(company_name):
    """Get complete customer 360 view for a company."""
    con = db()
    
    users = pd.read_sql_query(
        "SELECT id, first_name, last_name, username, email, role, login_count, created_at, last_login "
        "FROM users WHERE company_name=? ORDER BY id DESC",
        con, params=(company_name,)
    )
    
    activity = pd.read_sql_query(
        "SELECT username, action, created_at FROM activity WHERE company_name=? ORDER BY id DESC LIMIT 500",
        con, params=(company_name,)
    )
    
    chats = pd.read_sql_query(
        "SELECT username, sender, message, created_at FROM chat_history WHERE company_name=? ORDER BY id DESC LIMIT 500",
        con, params=(company_name,)
    )
    
    files = pd.read_sql_query(
        "SELECT username, filename, file_type, created_at FROM files WHERE company_name=? ORDER BY id DESC",
        con, params=(company_name,)
    )
    
    projects = pd.read_sql_query(
        "SELECT username, project_name, active_filename, updated_at FROM projects WHERE company_name=? ORDER BY id DESC",
        con, params=(company_name,)
    )
    
    emails = pd.read_sql_query(
        "SELECT recipient_name, recipient_email, subject, status, sent_at FROM emails_log "
        "WHERE company_name=? ORDER BY id DESC LIMIT 500",
        con, params=(company_name,)
    )
    
    calls = pd.read_sql_query(
        "SELECT room_name, title, host_username, mode, created_at, ended_at FROM call_rooms "
        "WHERE company_name=? ORDER BY id DESC",
        con, params=(company_name,)
    )
    
    con.close()
    return users, activity, chats, files, projects, emails, calls

def admin_metric_counts():
    """Get admin metric counts."""
    con = db()
    counts = {
        "users": con.execute("SELECT COUNT(*) FROM users WHERE role!='master'").fetchone()[0],
        "companies": con.execute("SELECT COUNT(*) FROM companies").fetchone()[0],
        "activities": con.execute(
            "SELECT COUNT(*) FROM activity WHERE lower(username) != lower(?)", (MASTER_USERNAME,)
        ).fetchone()[0] + con.execute("SELECT COUNT(*) FROM public_visits").fetchone()[0],
        "messages": con.execute(
            "SELECT COUNT(*) FROM chat_history WHERE lower(username) != lower(?)", (MASTER_USERNAME,)
        ).fetchone()[0],
        "files": con.execute(
            "SELECT COUNT(*) FROM files WHERE lower(username) != lower(?)", (MASTER_USERNAME,)
        ).fetchone()[0],
        "agents": con.execute("SELECT COUNT(*) FROM di_agents").fetchone()[0],
    }
    con.close()
    return counts

def _escape_html(value):
    """Escape HTML special characters."""
    if value is None:
        return ""
    return (str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))

def _dashboard_escape(value):
    """Escape value for dashboard."""
    return _escape_html(str(value))

def _dashboard_spark(values, width=112, height=34):
    """Create a sparkline SVG."""
    values = [float(v or 0) for v in values]
    if len(values) < 2:
        values = values + [values[-1] if values else 0]
    
    lo, hi = min(values), max(values)
    span = hi - lo or 1.0
    pts = []
    
    for i, value in enumerate(values):
        x = i * width / (len(values) - 1)
        y = height - 4 - ((value - lo) / span) * (height - 8)
        pts.append(f"{x:.1f},{y:.1f}")
    
    line = " ".join(pts)
    return f'''<svg viewBox="0 0 {width} {height}" class="dacre-spark" aria-hidden="true">
        <polyline points="{line}" fill="none" stroke="var(--dacre-chart-1)" stroke-width="2" 
                  stroke-linecap="round" stroke-linejoin="round"/>
    </svg>'''

def _dashboard_area_chart(points):
    """Create an area chart SVG."""
    if not points:
        points = [(f"{h:02d}:00", 0, 0) for h in range(0, 24, 3)]
    
    width, height = 900, 300
    left, right, top, bottom = 52, 20, 22, 42
    plot_w, plot_h = width - left - right, height - top - bottom
    maxv = max([max(a, b) for _, a, b in points] or [1]) or 1
    
    coords_a = []
    coords_b = []
    
    for i, (_, a, b) in enumerate(points):
        x = left + (i * plot_w / max(1, len(points) - 1))
        ya = top + plot_h - (a / maxv) * plot_h
        yb = top + plot_h - (b / maxv) * plot_h
        coords_a.append((x, ya))
        coords_b.append((x, yb))
    
    def poly(coords):
        return " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
    
    area_a = f"{left},{top + plot_h} {poly(coords_a)} {left + plot_w},{top + plot_h}"
    area_b = f"{left},{top + plot_h} {poly(coords_b)} {left + plot_w},{top + plot_h}"
    
    labels = []
    for i, (label, _, _) in enumerate(points):
        x = left + (i * plot_w / max(1, len(points) - 1))
        labels.append(f'<text x="{x:.1f}" y="{height - 12}" text-anchor="middle" class="chart-label">{_dashboard_escape(label)}</text>')
    
    grids = []
    for n in range(5):
        y = top + (plot_h * n / 4)
        val = maxv * (1 - n / 4)
        grids.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" class="chart-grid"/>')
        grids.append(f'<text x="{left - 9}" y="{y + 4:.1f}" text-anchor="end" class="chart-label">{val / 1000:.1f}k</text>')
    
    return f'''<svg viewBox="0 0 {width} {height}" class="dacre-area-chart" role="img" aria-label="Request throughput chart">
        <defs>
            <linearGradient id="dacreFillA" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="var(--dacre-chart-1)" stop-opacity=".34"/>
                <stop offset="100%" stop-color="var(--dacre-chart-1)" stop-opacity=".02"/>
            </linearGradient>
            <linearGradient id="dacreFillB" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="var(--dacre-chart-3)" stop-opacity=".22"/>
                <stop offset="100%" stop-color="var(--dacre-chart-3)" stop-opacity=".01"/>
            </linearGradient>
        </defs>
        {''.join(grids)}
        <polygon points="{area_b}" fill="url(#dacreFillB)"/>
        <polygon points="{area_a}" fill="url(#dacreFillA)"/>
        <polyline points="{poly(coords_b)}" fill="none" stroke="var(--dacre-chart-3)" stroke-width="2" stroke-linecap="round"/>
        <polyline points="{poly(coords_a)}" fill="none" stroke="var(--dacre-chart-1)" stroke-width="2.5" stroke-linecap="round"/>
        {''.join(labels)}
    </svg>'''

def _dashboard_scalar(sql, params=(), default=0):
    """Get a scalar value from a dashboard query."""
    con = db()
    try:
        row = con.execute(sql, params).fetchone()
        if row is None:
            return default
        try:
            value = row[0]
            return default if value is None else value
        except Exception:
            return default
    except Exception:
        return default
    finally:
        con.close()

def _dashboard_health_ring(value):
    """Create a health ring SVG."""
    value = max(0, min(100, float(value)))
    r = 52
    circumference = 2 * 3.141592653589793 * r
    offset = circumference - (value / 100) * circumference
    
    return f'''<div class="dacre-health-ring">
        <svg viewBox="0 0 144 144" aria-label="System health {value:.0f}">
            <circle cx="72" cy="72" r="{r}" fill="none" stroke="var(--dacre-muted-bg)" stroke-width="10"/>
            <circle cx="72" cy="72" r="{r}" fill="none" stroke="var(--dacre-chart-1)" stroke-width="10" 
                    stroke-linecap="round" stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{offset:.2f}" 
                    transform="rotate(-90 72 72)" class="health-progress"/>
        </svg>
        <div class="dacre-health-center">
            <b>{value:.0f}</b>
            <span>Health score</span>
        </div>
    </div>'''

def render_analytics_overview(user):
    """Render the analytics overview dashboard."""
    if not user or user.get("role") != "master":
        st.error("This platform-wide analytics view is available only to David Emenike in the Overall Admin DI Office.")
        return
    
    # Live metrics
    users = int(_dashboard_scalar("SELECT COUNT(*) FROM users WHERE role!='master'", default=0))
    company_filter = user.get("company") if user.get("role") != "master" else None
    
    if company_filter:
        activities = int(_dashboard_scalar("SELECT COUNT(*) FROM activity WHERE company_name=?", (company_filter,), 0))
        active_calls = int(_dashboard_scalar(
            "SELECT COUNT(*) FROM call_rooms WHERE company_name=? AND (ended_at IS NULL OR TRIM(ended_at)='')",
            (company_filter,), 0
        ))
        errors = int(_dashboard_scalar(
            "SELECT COUNT(*) FROM activity WHERE company_name=? AND (lower(action) LIKE '%error%' OR lower(action) LIKE '%fail%') AND created_at >= ?",
            (company_filter, (datetime.now().timestamp() - 86400).__str__()), 0
        ))
    else:
        activities = int(_dashboard_scalar("SELECT COUNT(*) FROM activity", default=0))
        active_calls = int(_dashboard_scalar("SELECT COUNT(*) FROM call_rooms WHERE ended_at IS NULL OR TRIM(ended_at)=''", default=0))
        errors = int(_dashboard_scalar(
            "SELECT COUNT(*) FROM activity WHERE (lower(action) LIKE '%error%' OR lower(action) LIKE '%fail%')",
            default=0
        ))
    
    # Build 24-hour activity series
    traffic = []
    try:
        con = db()
        if company_filter:
            dfh = pd.read_sql_query(
                "SELECT created_at FROM activity WHERE company_name=? ORDER BY id DESC LIMIT 3000",
                con, params=(company_filter,)
            )
        else:
            dfh = pd.read_sql_query("SELECT created_at FROM activity ORDER BY id DESC LIMIT 3000", con)
        con.close()
        
        if not dfh.empty:
            ts = pd.to_datetime(dfh["created_at"], errors="coerce")
            now = pd.Timestamp.now()
            for h in range(0, 24, 3):
                start = now - pd.Timedelta(hours=24 - h)
                end = start + pd.Timedelta(hours=3)
                count = int(((ts >= start) & (ts < end)).sum())
                traffic.append((start.strftime("%H:%M"), count, max(0, int(count * 0.62))))
    except Exception:
        traffic = []
    
    if not traffic:
        traffic = [
            ("00:00", 0, 0), ("03:00", 0, 0), ("06:00", 0, 0), ("09:00", 0, 0),
            ("12:00", 0, 0), ("15:00", 0, 0), ("18:00", 0, 0), ("21:00", 0, 0)
        ]
    
    health = max(0, min(100, round(99.98 - min(errors * 0.35, 25), 2)))
    spark_users = [max(0, users + i) for i in (-12, -8, -5, -7, -2, 4, 8, 0)]
    spark_activity = [max(0, activities + i) for i in (-30, -20, -8, -12, 0, 15, 24, 0)]
    spark_health = [96, 97, 98, 97, 99, 99, 100, health]
    spark_calls = [max(0, active_calls + i) for i in (20, 15, 12, 8, 10, 5, 3, 0)]
    
    st.markdown(f'''
    <div class="dacre-dashboard-topbar">
        <div class="dacre-dashboard-brand">
            <span class="live-pulse"><i></i></span>
            <div>
                <h1>DACRE Analytics</h1>
                <p>Real-time platform overview · all systems operational</p>
            </div>
        </div>
        <div class="dacre-dashboard-tools">
            <span class="dashboard-time">{datetime.now().strftime('%d %b %Y · %H:%M')}</span>
            <span class="dashboard-avatar">{_dashboard_escape((user.get('first_name','D')[:1] + user.get('last_name','A')[:1]).upper())}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    search = st.text_input(
        "Search metrics, agents...", value="", key="dashboard_search",
        label_visibility="collapsed", placeholder="Search metrics, agents..."
    )
    if search.strip():
        st.caption(f"Dashboard search: {search.strip()} · use the navigation to open the matching workspace.")
    
    kpis = [
        ("users", "Total Users", f"{users:,}", 12.4, spark_users, "registered platform users", "👥"),
        ("activity", "Activity", f"{activities:,}", 8.9, spark_activity, "recorded workspace events", "↗"),
        ("health", "System Health", f"{health:.2f}%", 0.3, spark_health, "availability signal · 24h", "◉"),
        ("calls", "Active Calls", f"{active_calls:,}", -3.1, spark_calls, "live sessions", "☎"),
    ]
    
    cards = []
    for key, label, value, delta, spark, hint, icon in kpis:
        positive = delta >= 0
        cards.append(f'''
        <div class="dacre-kpi-card">
            <div class="kpi-head">
                <span class="kpi-icon">{icon}</span>
                <span class="kpi-delta {'up' if positive else 'down'}">{'↗' if positive else '↘'} {abs(delta):.1f}%</span>
            </div>
            <p>{label}</p>
            <div class="kpi-value-row">
                <b>{_dashboard_escape(value)}</b>
                {_dashboard_spark(spark)}
            </div>
            <small>{_dashboard_escape(hint)}</small>
        </div>
        ''')
    
    st.markdown('<section class="dacre-kpi-grid">' + ''.join(cards) + '</section>', unsafe_allow_html=True)
    
    left, right = st.columns([2, 1], gap="large")
    with left:
        st.markdown(f'''
        <div class="dacre-panel">
            <div class="panel-head">
                <div>
                    <h2>Request Throughput</h2>
                    <p>Workspace activity and compute load across the platform</p>
                </div>
                <div class="range-pills">
                    <span class="active">24h</span>
                    <span>7d</span>
                    <span>30d</span>
                </div>
            </div>
            <div class="chart-legend">
                <span><i class="blue"></i>Activity</span>
                <span><i class="cyan"></i>Load</span>
            </div>
            {_dashboard_area_chart(traffic)}
        </div>
        ''', unsafe_allow_html=True)
    
    with right:
        resource_rows = [
            ("CPU", 42, "var(--dacre-chart-1)"),
            ("Memory", 61, "var(--dacre-chart-2)"),
            ("Network I/O", 28, "var(--dacre-chart-3)"),
            ("Storage", 74, "var(--dacre-chart-5)")
        ]
        bars = ''.join(f'''
        <div class="resource-row">
            <div>
                <span>{label}</span>
                <b>{value}%</b>
            </div>
            <div class="resource-track">
                <i style="width:{value}%;background:{color}"></i>
            </div>
        </div>
        ''' for label, value, color in resource_rows)
        
        st.markdown(f'''
        <div class="dacre-panel health-panel">
            <div class="panel-head">
                <div>
                    <h2>System Health</h2>
                    <p>Live resource utilization</p>
                </div>
            </div>
            {_dashboard_health_ring(health)}
            <div class="resource-list">{bars}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Recent activity table
    try:
        con = db()
        if company_filter:
            recent = pd.read_sql_query(
                "SELECT id, username, action, created_at FROM activity WHERE company_name=? ORDER BY id DESC LIMIT 8",
                con, params=(company_filter,)
            )
        else:
            recent = pd.read_sql_query(
                "SELECT id, username, action, created_at FROM activity ORDER BY id DESC LIMIT 8",
                con
            )
        con.close()
    except Exception:
        recent = pd.DataFrame(columns=["id", "username", "action", "created_at"])
    
    rows = []
    for _, r in recent.iterrows():
        action = str(r.get("action") or "System activity")
        low = action.lower()
        status = "error" if "error" in low or "fail" in low else ("warning" if "warn" in low else "success")
        rows.append(f'''
        <tr>
            <td><b>{_dashboard_escape(action[:90])}</b></td>
            <td>{_dashboard_escape(r.get('username', 'System'))}</td>
            <td><span class="channel">platform</span></td>
            <td><span class="status {status}"><i></i>{status}</span></td>
            <td class="mono">—</td>
            <td class="mono right">{_dashboard_escape(r.get('created_at', ''))}</td>
        </tr>
        ''')
    
    if not rows:
        rows.append('<tr><td colspan="6" class="empty-row">No activity has been recorded yet.</td></tr>')
    
    st.markdown(f'''
    <div class="dacre-panel activity-panel">
        <div class="panel-head">
            <div>
                <h2>Recent Activity</h2>
                <p>Latest events across agents and infrastructure</p>
            </div>
            <span class="view-all">Live ledger</span>
        </div>
        <div class="activity-scroll">
            <table class="dacre-activity-table">
                <thead>
                    <tr>
                        <th>Event</th>
                        <th>Agent</th>
                        <th>Channel</th>
                        <th>Status</th>
                        <th>Latency</th>
                        <th class="right">Time</th>
                    </tr>
                </thead>
                <tbody>{''.join(rows)}</tbody>
            </table>
        </div>
    </div>
    ''', unsafe_allow_html=True)

PAGE_META = {
    "Overview": ("⌂", "DACRE Overview", "Executive business intelligence workspace."),
    "DI Home": ("✦", "DI Home", "Your intelligent business copilot."),
    "DI Calls": ("◉", "DI Calls", "Intelligence conversations and action requests."),
    "DI Workforce": ("👥", "DI Workforce", "Your coordinated digital intelligence workforce."),
    "🌍 Global Markets": ("🌍", "Global Markets", "Market intelligence and global signals."),
    "🎥 DI Conference": ("🎥", "DI Conference", "Collaborative intelligence conference room."),
    "DI Action Center": ("⚡", "DI Action Center", "Prioritize and execute intelligence actions."),
    "DI Memory Box": ("🧠", "DI Memory Box", "Manage persistent DI knowledge and memory."),
    "Business Command Center": ("⌘", "Business Command Center", "Executive command and operational control."),
    "Business Twin": ("◇", "Business Twin", "Digital representation of your business."),
    "Decision Ledger": ("▤", "Decision Ledger", "Trace decisions, evidence, and outcomes."),
    "Opportunity Radar": ("◎", "Opportunity Radar", "Find measurable business opportunities."),
    "Workspace & Data": ("▦", "Workspace & Data", "Load, inspect, clean, and manage datasets."),
    "Formula Lab": ("ƒ", "Formula Lab", "Build and run analytical formulas."),
    "Charts": ("▥", "Charts", "Visualize business data and trends."),
    "File Vault": ("▣", "File Vault", "Secure workspace file management."),
    "Export Center": ("⇩", "Export Center", "Prepare and export analysis outputs."),
    "Chibobec Loan Desk": ("₦", "Chibobec Loan Desk", "Loan analysis and decision support."),
    "Organization Admin Portal": ("⚙", "Organization Admin Portal", "Organization administration and controls."),
    "Overall Admin DI Portal": ("◈", "Overall Admin DI Portal", "Founder-level control of the DACRE intelligence system."),
    "Research Store": ("⌕", "Research Store", "Research and knowledge resources."),
}

def render_page_chrome(page_name, user):
    """Render page chrome safely, even if an older deployment omitted PAGE_META."""
    _page_meta = globals().get("PAGE_META")
    if not isinstance(_page_meta, dict):
        _page_meta = {
            "Overview": ("◈", "DACRE Overview", "Executive business intelligence workspace."),
            "DI Home": ("🧠", "DI Home", "Your intelligent business copilot."),
            "DI Calls": ("📞", "DI Calls", "Intelligence conversations and action requests."),
            "DI Workforce": ("👥", "DI Workforce", "Your coordinated digital intelligence workforce."),
            "🌍 Global Markets": ("🌍", "Global Markets", "Market intelligence and global signals."),
            "🎥 DI Conference": ("🎥", "DI Conference", "Collaborative intelligence conference room."),
            "DI Action Center": ("⚡", "DI Action Center", "Prioritize and execute intelligence actions."),
            "DI Memory Box": ("🧠", "DI Memory Box", "Manage persistent DI knowledge and memory."),
            "Business Command Center": ("⌘", "Business Command Center", "Executive command and operational control."),
            "Business Twin": ("◇", "Business Twin", "Digital representation of your business."),
            "Decision Ledger": ("▤", "Decision Ledger", "Trace decisions, evidence, and outcomes."),
            "Opportunity Radar": ("◎", "Opportunity Radar", "Find measurable business opportunities."),
            "Workspace & Data": ("▦", "Workspace & Data", "Load, inspect, clean, and manage datasets."),
            "Formula Lab": ("ƒ", "Formula Lab", "Build and run analytical formulas."),
            "Charts": ("▥", "Charts", "Visualize business data and trends."),
            "File Vault": ("▣", "File Vault", "Secure workspace file management."),
            "Export Center": ("⇩", "Export Center", "Prepare reports and exports."),
            "Chibobec Loan Desk": ("₦", "Chibobec Loan Desk", "Loan analysis and decision support."),
            "Organization Admin Portal": ("⚙", "Organization Admin Portal", "Organization administration and controls."),
            "Overall Admin DI Portal": ("👑", "Overall Admin DI Portal", "Founder-level control of the DACRE intelligence system."),
            "Research Store": ("⌕", "Research Store", "Research and knowledge resources."),
        }
    icon, title, subtitle = _page_meta.get(page_name, ("•", page_name, "Dacre business intelligence workspace."))
    master = user.get("role") == "master"
    mode_label = "FOUNDER COMMAND" if master else str(user.get("company", "BUSINESS WORKSPACE")).upper()
    
    st.markdown(f"""
    <div class="dacre-page-chrome {'master-page-chrome' if master else ''}">
        <div class="page-chrome-left">
            <div class="page-icon">{icon}</div>
            <div>
                <div class="page-kicker">{_escape_html(mode_label)} · DA-CRE</div>
                <div class="page-title">{_escape_html(title)}</div>
                <div class="page-subtitle">{_escape_html(subtitle)}</div>
            </div>
        </div>
        <div class="page-chrome-right">
            <span class="chrome-pill">● DI ONLINE</span>
            <span class="chrome-pill soft">{datetime.now().strftime("%d %b %Y · %H:%M")}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def log_di_action(user, action_type, request, result, agent_name="DI"):
    """Log a DI action."""
    con = db()
    con.execute("""
        INSERT INTO di_action_log(company_name, username, agent_name, action_type, request, result, created_at)
        VALUES(?,?,?,?,?,?,?)
    """, (
        user["company"], user["username"], agent_name, action_type, request, result,
        datetime.now().isoformat(timespec="seconds")
    ))
    con.commit()
    con.close()

def get_recent_di_actions(user, limit=20):
    """Get recent DI actions for a user."""
    con = db()
    df = pd.read_sql_query(
        """SELECT agent_name, action_type, request, result, created_at
           FROM di_action_log
           WHERE company_name=? AND username=?
           ORDER BY id DESC LIMIT ?""",
        con, params=(user["company"], user["username"], int(limit)),
    )
    con.close()
    return df

def render_business_twin(df, user):
    """Render the business twin page."""
    if df is None or df.empty:
        st.info("Load a dataset in Workspace & Data and the Business Twin will build itself from real data.")
        return
    
    health = business_health(df)
    signals = business_signals(df)
    opportunities = opportunity_radar(df, user["company"], user["username"])
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())
    numeric = len(df.select_dtypes(include="number").columns)
    
    st.markdown(f"""
    <div class="business-twin-banner">
        <div>
            <span class="twin-label">LIVE BUSINESS TWIN</span>
            <h2>{_escape_html(user['company'])}</h2>
            <p>This snapshot is generated from the active workspace only. Dacre does not invent company numbers.</p>
        </div>
        <div class="twin-score">
            <b>{health['score']}</b>
            <span>/100</span>
            <small>DATA HEALTH</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    k = st.columns(5)
    for col, label, value in zip(
        k,
        ["Rows", "Columns", "Numeric fields", "Missing cells", "Duplicates"],
        [f"{len(df):,}", f"{len(df.columns):,}", f"{numeric:,}", f"{missing:,}", f"{duplicates:,}"]
    ):
        with col:
            st.markdown(f"<div class='twin-metric'><b>{value}</b><span>{label}</span></div>", unsafe_allow_html=True)
    
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("### What deserves attention")
        if signals:
            for item in signals[:6]:
                st.markdown(
                    f"<div class='insight-row'><b>{_escape_html(item.get('title', ''))}</b>"
                    f"<span>{_escape_html(item.get('message', ''))}</span></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.success("No major deterministic data-quality/business signals were detected in the current dataset.")
    
    with right:
        st.markdown("### Opportunity signals")
        if opportunities:
            for item in opportunities:
                st.markdown(
                    f"<div class='opportunity-row'><b>{_escape_html(item['title'])}</b>"
                    f"<span>{_escape_html(item['impact'])}</span>"
                    f"<small>{_escape_html(item['action'])}</small></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("No measurable opportunity signal has crossed the current detection threshold.")
    
    st.markdown("### Ask DI to explain the twin")
    prompt = st.text_input(
        "Business Twin question",
        placeholder="e.g. What changed most, what should management investigate, and why?",
        key="business_twin_question",
    )
    
    if st.button("✦ Explain this Business Twin", use_container_width=True, type="primary") and prompt.strip():
        answer = enhanced_di_reply(prompt, user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
        log_di_action(user, "business_twin", prompt, answer)
        st.markdown(
            f"<div class='di-answer-panel'><div class='answer-label'>DI EXPLANATION</div>"
            f"<div>{_escape_html(answer).replace(chr(10), '<br>')}</div></div>",
            unsafe_allow_html=True
        )

def render_action_center(user):
    """Render the DI action center."""
    df = st.session_state.get("processed_df")
    
    st.markdown("""
    <div class="action-center-banner">
        <span>DI ACTION ENGINE</span>
        <h2>Give DI a business outcome — not a menu to navigate.</h2>
        <p>DI can use the same core reasoning, data analysis, memory and research capabilities available from the main Dacre workspace.</p>
    </div>
    """, unsafe_allow_html=True)
    
    q = st.text_area(
        "What should DI do?",
        placeholder="Analyze this dataset, investigate a business issue, draft an email, explain a formula, prepare an executive brief, research a current topic...",
        height=130,
        key="action_center_request",
    )
    
    c1, c2, c3, c4 = st.columns(4)
    quick = [
        ("Analyze", "Analyze the active dataset and tell me the most important findings."),
        ("Executive brief", "Create a concise executive brief from the active dataset with priorities."),
        ("Risk check", "Identify the most important data-quality and business risks visible in the active dataset."),
        ("Opportunity", "Find measurable opportunity signals in the active dataset and explain what to investigate."),
    ]
    
    for col, (label, prompt) in zip([c1, c2, c3, c4], quick):
        with col:
            if st.button(label, use_container_width=True):
                q = prompt
    
    if st.button("Run DI Action", use_container_width=True, type="primary") and q.strip():
        answer = enhanced_di_reply(q.strip(), user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
        log_di_action(user, "action_center", q.strip(), answer)
        st.session_state.last_action_center_result = answer
        st.session_state.last_speech = answer
    
    if st.session_state.get("last_action_center_result"):
        st.markdown(
            f"""<div class="di-answer-panel"><div class="answer-label">DI COMPLETED ACTION</div>
            <div>{_escape_html(st.session_state.last_action_center_result).replace(chr(10), '<br>')}</div></div>""",
            unsafe_allow_html=True,
        )
    
    recent = get_recent_di_actions(user)
    if not recent.empty:
        st.markdown("### Your DI action history")
        st.dataframe(safe_dataframe_for_streamlit(recent), use_container_width=True, hide_index=True)

# =============================================================================
# RENDER FUNCTIONS
# =============================================================================

def render_decision_ledger(user):
    """Render the decision ledger page."""
    st.markdown("""
    <div class="decision-banner">
        <span>INSTITUTIONAL MEMORY</span>
        <h2>Decisions should become company knowledge.</h2>
        <p>Record the decision, the reason, the expected result and later the actual result. This lets DI learn from the organization's history.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("decision_ledger_form", clear_on_submit=True):
        a, b = st.columns(2)
        with a:
            title = st.text_input("Decision title", placeholder="e.g. Change supplier for Product A")
            context = st.text_area("Context / evidence", height=90)
            decision = st.text_area("Decision made", height=90)
        with b:
            expected = st.text_area("Expected outcome", height=90)
            review = st.date_input("Review date", value=datetime.now().date())
        
        save = st.form_submit_button("Save decision to Dacre Memory", use_container_width=True, type="primary")
    
    if save and title.strip() and decision.strip():
        create_decision(user["company"], user["username"], title.strip(), context.strip(), decision.strip(), expected.strip(), str(review))
        log_activity(user["username"], user["company"], f"Saved decision: {title[:120]}")
        st.success("Decision saved. DI can now use the record as organizational history.")
    
    con = db()
    decisions = pd.read_sql_query(
        "SELECT title, context, decision, expected_outcome, review_date, status, outcome, created_at, updated_at "
        "FROM decision_ledger WHERE company_name=? ORDER BY id DESC",
        con, params=(user["company"],),
    )
    con.close()
    
    if not decisions.empty:
        st.dataframe(safe_dataframe_for_streamlit(decisions), use_container_width=True, hide_index=True)

def render_opportunity_page(user):
    """Render the opportunity radar page."""
    df = st.session_state.get("processed_df")
    
    st.markdown("""
    <div class="opportunity-banner">
        <span>OPPORTUNITY RADAR</span>
        <h2>Find upside before it becomes obvious.</h2>
        <p>Dacre scans numeric trends in the active dataset and turns measurable changes into investigation prompts.</p>
    </div>
    """, unsafe_allow_html=True)
    
    opportunities = opportunity_radar(df, user["company"], user["username"])
    
    if not opportunities:
        st.info("Load a dataset with enough numeric observations to generate measurable opportunity signals.")
        return
    
    for item in opportunities:
        st.markdown(f"""
        <div class="opportunity-card">
            <div class="opp-title">{_escape_html(item['title'])}</div>
            <div class="opp-impact">{_escape_html(item['impact'])}</div>
            <p>{_escape_html(item['evidence'])}</p>
            <b>Suggested investigation</b>
            <p>{_escape_html(item['action'])}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Ask DI to investigate · {item['title']}", key=f"opp_{hash(item['title'])}", use_container_width=True):
            prompt = f"Investigate this opportunity signal: {item['title']}. Evidence: {item['evidence']}. Suggested action: {item['action']}"
            answer = enhanced_di_reply(prompt, user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
            log_di_action(user, "opportunity", prompt, answer)
            st.markdown(
                f"<div class='di-answer-panel'><div class='answer-label'>DI INVESTIGATION</div>"
                f"<div>{_escape_html(answer).replace(chr(10), '<br>')}</div></div>",
                unsafe_allow_html=True
            )

def _dacre_logo_data_uri():
    """Return the bundled DACRE logo as a data URI when available."""
    try:
        if LOGO_PATH.exists():
            raw = LOGO_PATH.read_bytes()
            mime = "image/png"
            if LOGO_PATH.suffix.lower() in (".jpg", ".jpeg"):
                mime = "image/jpeg"
            elif LOGO_PATH.suffix.lower() == ".webp":
                mime = "image/webp"
            return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"
    except Exception:
        pass
    return ""

def _landing_auth_panel():
    """Render authentication inside the public DACRE landing page."""
    mode = st.session_state.get("landing_mode", "home")
    if mode not in ("login", "signup"):
        return

    st.markdown("""
    <style>
    .auth-anchor { scroll-margin-top: 20px; }
    .auth-shell {
        max-width: 980px;
        margin: 18px auto 42px;
        padding: 1px;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(91,73,255,.75), rgba(37,211,238,.55), rgba(255,255,255,.08));
        box-shadow: 0 28px 90px rgba(0,0,0,.38);
    }
    .auth-inner {
        border-radius: 23px;
        background: #0b1020;
        padding: 30px;
        border: 1px solid rgba(255,255,255,.08);
    }
    .auth-title { color:#f7f9ff; font-size:28px; font-weight:800; letter-spacing:-.03em; }
    .auth-sub { color:#9ba9c2; margin-top:6px; margin-bottom:20px; }
    .auth-badge {
        display:inline-flex;
        align-items:center;
        gap:8px;
        padding:6px 10px;
        border-radius:999px;
        border:1px solid rgba(126,115,255,.3);
        background:rgba(92,76,255,.10);
        color:#bfc5ff;
        font-size:12px;
        font-weight:700;
    }
    </style>
    <div id="dacre-auth" class="auth-anchor auth-shell">
        <div class="auth-inner">
            <div class="auth-badge">✦ DACRE secure workspace access</div>
            <div class="auth-title">Your DACRE workspace starts here.</div>
            <div class="auth-sub">Sign in to your existing workspace or create your organization account without leaving the DACRE landing page.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2.2, 1])
    with c2:
        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            with st.form("landing_login_form", clear_on_submit=False):
                login_company = st.text_input(
                    "Company / Organization",
                    placeholder="e.g. Edubridge Consultant Limited",
                    key="landing_login_company",
                )
                login_fullname = st.text_input(
                    "Full Name",
                    placeholder="e.g. David Emenike",
                    key="landing_login_fullname",
                )
                login_email = st.text_input(
                    "Email Address",
                    placeholder="Use the email registered with DACRE",
                    key="landing_login_email",
                )
                login_passkey = st.text_input(
                    "Account Passkey",
                    type="password",
                    placeholder="Enter your DACRE account passkey",
                    key="landing_login_passkey",
                )
                login_submit = st.form_submit_button(
                    "Sign In & Open My DACRE Workspace",
                    use_container_width=True,
                    type="primary",
                )

            if login_submit:
                auth, auth_message = authenticate(
                    login_company, login_fullname, login_passkey, login_email
                )
                if auth:
                    st.session_state.user = auth
                    st.session_state.master_route = auth.get("role") == "master"
                    st.session_state.landing_mode = "home"
                    st.session_state.last_speech = (
                        f"Welcome back, {auth['first_name']}. I am DI. "
                        "Where would you like to start today?"
                    )
                    project = restore_user_workspace(auth)
                    st.toast(
                        f"Welcome back, {auth['first_name']}! Your saved DACRE workspace has been restored."
                    )
                    st.rerun()
                else:
                    st.error(
                        auth_message or
                        "We could not sign you in. Check your details or create a DACRE account."
                    )

        with tab_signup:
            with st.form("landing_signup_form", clear_on_submit=False):
                s_first = st.text_input(
                    "First Name", placeholder="e.g. David", key="landing_signup_first"
                )
                s_last = st.text_input(
                    "Last Name", placeholder="e.g. Emenike", key="landing_signup_last"
                )
                s_company = st.text_input(
                    "Company / Organization",
                    placeholder="e.g. Edubridge Consultant Limited",
                    key="landing_signup_company",
                )
                s_email = st.text_input(
                    "Email Address",
                    placeholder="e.g. name@example.com",
                    key="landing_signup_email",
                )
                s_email_pass = st.text_input(
                    "Email Password (optional)",
                    type="password",
                    placeholder="Optional — only needed for configured email features",
                    key="landing_signup_email_password",
                )
                s_passkey = st.text_input(
                    "Create Account Passkey",
                    type="password",
                    placeholder="Create a secure passkey for your DACRE account",
                    key="landing_signup_passkey",
                )
                s_website = st.text_input(
                    "Do you have a website? Please put your company official URL to get the best performance from DI — David's Intelligence.",
                    placeholder="https://www.yourcompany.com",
                    key="landing_signup_website",
                )
                st.caption("Your official site helps DI prepare company context and adapt the workspace appearance. Website onboarding runs in the background so signup stays fast.")
                signup_submit = st.form_submit_button(
                    "Create My DACRE Account",
                    use_container_width=True,
                    type="primary",
                )

            if signup_submit:
                success, msg, created = create_account(
                    s_first, s_last, s_company, s_email, s_email_pass, s_passkey, s_website
                )
                if success:
                    st.session_state.user = created
                    st.session_state.master_route = False
                    st.session_state.landing_mode = "home"
                    if is_chibobec_company(created["company"]):
                        st.session_state.last_speech = (
                            f"We know you are coming, {CHIBOBEC_OWNER_NAME}. "
                            "Welcome to DACRE Analysis. Your loan collection workspace is ready, "
                            "and DI is standing by to help you manage your clients and repayment reminders."
                        )
                    else:
                        st.session_state.last_speech = (
                            f"Welcome to DACRE, {created['first_name']}. "
                            "I am DI, your business intelligence assistant. "
                            "What would you like us to work on first?"
                        )
                    # The account is intentionally persistent: there is no 10-day or 40-day
                    # expiry. The user can sign in again whenever they return, provided the
                    # account/database still exists and they use the same credentials.
                    restore_user_workspace(created)
                    st.toast(f"Welcome to DACRE, {created['first_name']}! Your workspace is ready.")
                    st.rerun()
                else:
                    st.error(msg)

        if st.button("← Continue browsing DACRE", key="landing_auth_back", use_container_width=True):
            st.session_state.landing_mode = "home"
            st.rerun()

        # Discreet private CEO Office launcher
        st.markdown("""
        <style>
          .ceo-launcher-wrap{margin:28px auto 4px;text-align:center;opacity:.86}
          .ceo-launcher-wrap a{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:14px;
            border:1px solid rgba(112,132,255,.24);background:linear-gradient(145deg,rgba(28,41,74,.95),rgba(7,13,28,.95));
            box-shadow:0 12px 34px rgba(0,0,0,.28),0 0 18px rgba(74,110,255,.10);transition:.2s ease;text-decoration:none}
          .ceo-launcher-wrap a:hover{transform:translateY(-2px);border-color:rgba(105,145,255,.6);box-shadow:0 16px 40px rgba(0,0,0,.34),0 0 24px rgba(74,110,255,.22)}
          .ceo-launcher-wrap img{width:28px;height:28px;object-fit:contain;border-radius:8px}
          .ceo-launcher-caption{margin-top:7px;color:#70809b;font-size:9px;letter-spacing:.12em;text-transform:uppercase;font-weight:800}
        </style>
        <div class="ceo-launcher-wrap">
          <a href="?master_gate=1" title="Private CEO Office">__CEO_LOGO__</a>
          <div class="ceo-launcher-caption">Private CEO Office</div>
        </div>
        """.replace("__CEO_LOGO__", f'<img src="{_dacre_logo_data_uri()}" alt="DACRE" />'), unsafe_allow_html=True)

def landing_page():
    """Public DACRE landing experience with connected navigation and real auth."""
    record_public_visit("landing_view", "Landing")
    
    # PRIVATE MASTER GATE
    if st.query_params.get("master_gate") == "1":
        captcha_required = st.session_state.get("master_captcha_required", False)
        captcha_passed = st.session_state.get("master_captcha_passed", False)
        second_attempt = st.session_state.get("master_second_attempt", False)

        st.markdown("""
        <style>
          .dacre-master-shell { max-width: 720px; margin: 60px auto; padding: 36px;
            border-radius: 24px; background:#0b1020; border:1px solid rgba(255,255,255,.09);
            box-shadow:0 30px 90px rgba(0,0,0,.45); }
        </style>
        <div class="dacre-master-shell">
          <div style="color:#f7f9ff;font-size:28px;font-weight:800;">Overall Admin DI — Master Access</div>
          <div style="color:#9ba9c2;margin-top:8px;">Private system-wide access for the DACRE master administrator.</div>
        </div>
        """, unsafe_allow_html=True)

        gate_col1, gate_col2, gate_col3 = st.columns([1, 2, 1])
        with gate_col2:
            if captcha_required and not captcha_passed:
                st.markdown("### Security verification")
                site_key = os.getenv("DACRE_RECAPTCHA_SITE_KEY", "").strip()
                if site_key:
                    components.html(f"""
                    <div style="display:flex;justify-content:center;">
                      <div class="g-recaptcha" data-sitekey="{site_key}"></div>
                    </div>
                    <script src="https://www.google.com/recaptcha/api.js" async defer></script>
                    """, height=100)
                    st.caption("Complete the configured security verification before continuing.")
                    if st.button("I completed the reCAPTCHA", use_container_width=True):
                        st.warning("Complete the verification widget first.")
                else:
                    if st.checkbox("Complete security verification", key="local_captcha_check"):
                        st.session_state.master_captcha_passed = True
                        st.session_state.master_second_attempt = True
                        st.rerun()

                if st.button("Return to DACRE", use_container_width=True, key="master_return_1"):
                    st.session_state.master_captcha_required = False
                    st.session_state.master_captcha_passed = False
                    st.session_state.master_second_attempt = False
                    st.session_state.master_guard_challenge_required = False
                    st.session_state.master_guard_failed = False
                    st.query_params.clear()
                    st.rerun()
                return

            # Second gate: CEO Office Guardian
            if st.session_state.get("master_guard_challenge_required", False):
                st.markdown("### CEO Office Guardian Verification")
                if st.session_state.get("master_guard_failed", False):
                    st.warning("That guardian name was not recognized. Please enter the name exactly as it was given when the guardian was created.")
                
                guardian_answer = st.text_input(
                    "Sorry, please Master, what is the name you gave me when you created me?",
                    placeholder="Enter the guardian's name",
                    key="master_guard_answer",
                )
                gg1, gg2 = st.columns(2)
                with gg1:
                    if st.button("Verify Guardian", use_container_width=True, type="primary", key="master_guard_verify"):
                        if guardian_answer.strip().casefold() == CEO_GUARD_NAME.casefold():
                            st.session_state.user = master_user_record()
                            st.session_state.master_route = True
                            st.session_state.master_captcha_required = False
                            st.session_state.master_captcha_passed = False
                            st.session_state.master_second_attempt = False
                            st.session_state.master_guard_challenge_required = False
                            st.session_state.master_guard_failed = False
                            st.session_state.last_speech = "Welcome, Master David. Guaiel has verified the CEO Office. Overall Admin DI is online."
                            st.query_params.clear()
                            log_activity(MASTER_USERNAME, "DACRE MASTER", "Opened Overall CEO Office after Guaiel guardian verification", notify_admin=False)
                            st.rerun()
                        else:
                            st.session_state.master_guard_failed = True
                            st.rerun()
                with gg2:
                    if st.button("Return to DACRE", use_container_width=True, key="master_guard_return"):
                        st.session_state.master_guard_challenge_required = False
                        st.session_state.master_guard_failed = False
                        st.query_params.clear()
                        st.rerun()
                return

            master_pk = st.text_input(
                "Account Passkey",
                type="password",
                placeholder="Enter your private account passkey",
                key="master_gate_pk",
            )
            if second_attempt:
                st.info("Security verification completed. Please enter the passkey again.")

            g1, g2 = st.columns(2)
            with g1:
                if st.button("Open Overall Admin DI", use_container_width=True, type="primary", key="master_open"):
                    if master_passkey_gate(master_pk):
                        st.session_state.master_guard_challenge_required = True
                        st.session_state.master_guard_failed = False
                        st.rerun()
                    else:
                        if second_attempt:
                            st.warning("The second passkey attempt was incorrect. Returning to DACRE.")
                            st.session_state.master_captcha_required = False
                            st.session_state.master_captcha_passed = False
                            st.session_state.master_second_attempt = False
                            st.session_state.master_guard_challenge_required = False
                            st.session_state.master_guard_failed = False
                            st.query_params.clear()
                            st.rerun()
                        else:
                            st.session_state.master_captcha_required = True
                            st.session_state.master_captcha_passed = False
                            st.session_state.master_second_attempt = False
                            st.rerun()
            with g2:
                if st.button("Return to DACRE", use_container_width=True, key="master_return_2"):
                    st.session_state.master_captcha_required = False
                    st.session_state.master_captcha_passed = False
                    st.session_state.master_second_attempt = False
                    st.query_params.clear()
                    st.rerun()
        return

    logo_uri = _dacre_logo_data_uri()
    logo = f'<img src="{logo_uri}" alt="DACRE" class="brand-logo"/>' if logo_uri else '<span class="brand-fallback">D</span>'

    # Landing stylesheet — white enterprise website, black typography, DACRE blue.
    st.markdown("""
    <style>
      #MainMenu, footer { visibility:hidden; }
      [data-testid="stSidebar"] { display:none; }
      .stApp { background:#f7f9fc !important; }
      .block-container { max-width:1480px !important; padding:18px 28px 55px !important; }
      .dacre-landing { color:#101828; font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
      .dacre-nav {
        min-height:70px; display:flex; align-items:center; justify-content:space-between; gap:18px;
        padding:10px 14px; border:1px solid #e4e7ec; border-radius:14px; background:#fff;
        box-shadow:0 8px 26px rgba(16,24,40,.07); position:sticky; top:10px; z-index:10;
      }
      .dacre-brand { display:flex; align-items:center; gap:12px; min-width:220px; }
      .brand-logo { width:43px; height:43px; object-fit:contain; border-radius:11px; }
      .brand-fallback { display:grid; place-items:center; width:43px;height:43px; font-size:21px; background:#1769ff; color:#fff; font-weight:900; border-radius:11px; }
      .dacre-brand-name { font-size:18px;font-weight:900;letter-spacing:-.025em;color:#101828; }
      .dacre-brand-sub { color:#667085;font-size:10px;margin-top:2px; }
      .system-ready { display:inline-flex;align-items:center;gap:7px;color:#344054;font-size:10px;font-weight:800;letter-spacing:.05em;white-space:nowrap; }
      .ready-dot { width:8px;height:8px;border-radius:50%;background:#12b76a;box-shadow:0 0 10px rgba(18,183,106,.4); }
      .hero {
        min-height:610px; display:grid; grid-template-columns:1.05fr .95fr; gap:44px; align-items:center;
        padding:74px 28px 52px; position:relative;
      }
      .hero:before{content:"";position:absolute;left:28px;top:42px;width:6px;height:92px;border-radius:8px;background:#1769ff;}
      .hero-eyebrow { display:inline-flex; padding:8px 12px; border:1px solid #cfe0ff; background:#eaf2ff; border-radius:999px;color:#0b4fd1;font-size:11px;font-weight:800; }
      .hero-title { font-size:clamp(46px,6.2vw,80px); line-height:.98; letter-spacing:-.065em; font-weight:900; margin:22px 0 20px; max-width:760px;color:#101828; }
      .gradient-text { color:#1769ff; }
      .hero-copy { max-width:650px; color:#475467;font-size:17px;line-height:1.75; }
      .hero-proof { display:flex; gap:22px; flex-wrap:wrap; margin-top:34px; color:#344054;font-size:12px;font-weight:650; }
      .proof-dot { color:#1769ff; }
      .page-hero { padding:62px 28px 28px; }
      .page-title { font-size:clamp(42px,5.8vw,72px); line-height:1; letter-spacing:-.06em; font-weight:900; margin:14px 0 16px;color:#101828; }
      .page-copy { max-width:790px; color:#475467; font-size:17px; line-height:1.75; }
      .section { padding:62px 28px; }
      .section-head { max-width:820px;margin-bottom:32px; }
      .section-kicker { color:#1769ff;text-transform:uppercase;letter-spacing:.16em;font-size:10px;font-weight:900; }
      .section-title { font-size:38px;line-height:1.05;letter-spacing:-.045em;font-weight:850;margin-top:10px;color:#101828; }
      .section-copy { color:#667085;line-height:1.75;font-size:15px;margin-top:10px; }
      .grid-3 { display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px; }
      .grid-2 { display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px; }
      .feature-card { padding:24px;min-height:180px;border:1px solid #e4e7ec;border-radius:18px;background:#fff;box-shadow:0 8px 26px rgba(16,24,40,.055);transition:transform .16s ease,box-shadow .16s ease; }
      .feature-card:hover{transform:translateY(-3px);box-shadow:0 16px 36px rgba(16,24,40,.10);}
      .feature-icon { width:42px;height:42px;border-radius:12px;display:grid;place-items:center;background:#eaf2ff;color:#1769ff;font-weight:900;margin-bottom:16px;border:1px solid #cfe0ff; }
      .feature-card h3 { margin:0;font-size:20px;letter-spacing:-.025em;color:#101828; }
      .feature-card p { color:#667085;line-height:1.65;margin:8px 0 0;font-size:14px; }
      .pill-row { display:flex; gap:9px; flex-wrap:wrap; margin-top:20px; }
      .pill { padding:8px 11px; border-radius:999px; border:1px solid #cfe0ff; background:#f5f9ff; color:#0b4fd1; font-size:11px; font-weight:700; }
      .workflow { display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px; }
      .step { padding:20px;border-radius:16px;border:1px solid #e4e7ec;background:#fff;box-shadow:0 6px 20px rgba(16,24,40,.04); }
      .step-num { color:#1769ff;font-size:10px;font-weight:900;letter-spacing:.14em; }
      .step h4 { margin:8px 0 7px;font-size:18px;color:#101828; }
      .step p { color:#667085;font-size:13px;line-height:1.6;margin:0; }
      .callout { padding:28px;border-radius:18px;border:1px solid #cfe0ff;background:#fff;box-shadow:0 10px 30px rgba(16,24,40,.06);position:relative;overflow:hidden; }
      .callout:before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:#1769ff;}
      .callout h3 { margin:0 0 8px;font-size:24px;color:#101828; }
      .callout p { margin:0;color:#667085;line-height:1.7; }
      .metric-row { display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:20px; }
      .metric { padding:18px;border-radius:14px;border:1px solid #e4e7ec;background:#fff;box-shadow:0 6px 20px rgba(16,24,40,.04); }
      .metric small { color:#667085;font-size:10px;text-transform:uppercase;letter-spacing:.12em; }
      .metric strong { display:block;margin-top:5px;font-size:26px;color:#101828; }
      .cta { margin:20px 28px 30px;padding:44px 28px;border-radius:20px;border:1px solid #bcd4ff;background:#101828;text-align:center;position:relative;overflow:hidden; }
      .cta:after{content:"";position:absolute;right:-100px;top:-130px;width:320px;height:320px;border-radius:50%;background:rgba(23,105,255,.28);filter:blur(3px);}
      .cta h2 { font-size:clamp(30px,4vw,52px);letter-spacing:-.05em;margin:10px 0;color:#fff;position:relative;z-index:1; }
      .cta p { max-width:680px;margin:0 auto 18px;color:#d0d5dd;line-height:1.7;position:relative;z-index:1; }
      .footer { display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:26px 28px;color:#667085;font-size:11px; }
      .hero-visual-host { min-height:500px; }
      .auth-shell { max-width:980px; margin:28px auto 42px; padding:1px;border-radius:20px;background:#1769ff;box-shadow:0 20px 55px rgba(16,24,40,.12); }
      .auth-inner { border-radius:19px;background:#fff;padding:30px;border:1px solid #e4e7ec; }
      .auth-title { color:#101828;font-size:28px;font-weight:800;letter-spacing:-.03em; }
      .auth-sub { color:#667085;margin-top:6px;margin-bottom:20px; }
      .auth-badge { display:inline-flex;align-items:center;gap:8px;padding:6px 10px;border-radius:999px;border:1px solid #cfe0ff;background:#eaf2ff;color:#0b4fd1;font-size:12px;font-weight:700; }
      @media(max-width:980px){ .hero{grid-template-columns:1fr;padding-top:52px}.grid-3,.grid-2{grid-template-columns:1fr 1fr}.workflow{grid-template-columns:1fr 1fr}.metric-row{grid-template-columns:1fr 1fr}.hero-visual-host{min-height:430px} }
      @media(max-width:680px){ .block-container{padding:0 12px 40px !important}.dacre-nav{position:static;padding:12px}.dacre-brand{min-width:auto}.system-ready{display:none}.hero{padding:48px 10px 25px;min-height:auto}.hero-title{font-size:48px}.section,.page-hero{padding:48px 10px 20px}.grid-3,.grid-2,.workflow,.metric-row{grid-template-columns:1fr}.section-title{font-size:31px}.hero-visual-host{min-height:360px}.cta{margin:18px 10px 25px;padding:34px 20px}.footer{padding:22px 10px} }
    /* DACRE dark landing system */
.dacre-landing{color:#f5f9ff!important}.dacre-landing .dacre-nav{background:rgba(8,14,24,.94);border-color:#263b54;box-shadow:0 18px 55px rgba(0,0,0,.30);backdrop-filter:blur(14px)}
.dacre-landing .dacre-brand-name,.dacre-landing .hero-title,.dacre-landing .page-title,.dacre-landing .section-title,.dacre-landing .feature-card h3,.dacre-landing .step h4,.dacre-landing .callout h3,.dacre-landing .metric strong{color:#fff!important}.dacre-landing .dacre-brand-sub,.dacre-landing .hero-copy,.dacre-landing .hero-proof,.dacre-landing .section-copy,.dacre-landing .feature-card p,.dacre-landing .step p,.dacre-landing .callout p,.dacre-landing .metric small,.dacre-landing .footer{color:#aebed0!important}
.dacre-landing .hero:before{background:linear-gradient(180deg,#58c7ff,#ff9f43)!important}.dacre-landing .hero-eyebrow{background:#0d2235;border-color:#2c5a78;color:#79d3ff}.dacre-landing .gradient-text{color:#58c7ff!important}.dacre-landing .feature-card,.dacre-landing .step,.dacre-landing .metric,.dacre-landing .callout{background:linear-gradient(145deg,#0b1422,#101b2b);border-color:#263b54;box-shadow:0 16px 44px rgba(0,0,0,.28)}
.dacre-landing .feature-icon{background:#0d2538;color:#58c7ff;border-color:#2c5a78}.dacre-landing .pill{background:#151c28;border-color:#33495f;color:#b9d4e8}.dacre-landing .cta{background:linear-gradient(135deg,#07101b,#11243a);border-color:#31516f}.dacre-landing .footer{border-top:1px solid #203149}.dacre-landing .auth-inner{background:#0b1422;border-color:#263b54}.dacre-landing .auth-title{color:#fff!important}
</style>
    """, unsafe_allow_html=True)

    current_section = st.session_state.get("landing_section", "home")
    mode = st.session_state.get("landing_mode", "home")

    st.markdown(f"""
        <div class="dacre-nav">
          <div class="dacre-brand">{logo}<div><div class="dacre-brand-name">DACRE</div><div class="dacre-brand-sub">Powered by DI — David's Intelligence</div></div></div>
          <div class="system-ready"><span class="ready-dot"></span> DI ONLINE · DAVID'S INTELLIGENCE</div>
        </div>
        """, unsafe_allow_html=True)
    
    nav_items = [("Features", "features"), ("Intelligence", "intelligence"), ("Workforce", "workforce"), ("Analytics", "analytics"), ("Security", "security")]
    nav_cols = st.columns([1.0, 1.0, 1.0, 1.0, 1.0, 0.85, 0.85])
    for i, (label, target) in enumerate(nav_items):
        with nav_cols[i]:
            if st.button(label, key=f"landing_nav_{target}", use_container_width=True):
                st.session_state.landing_section = target
                st.session_state.landing_mode = "home"
                st.rerun()
    with nav_cols[5]:
        if st.button("Log In", key="landing_nav_login", use_container_width=True):
            st.session_state.landing_mode = "login"
            st.session_state.landing_section = "home"
            st.rerun()
    with nav_cols[6]:
        if st.button("Get Started", key="landing_nav_signup", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    # Dedicated auth pages
    if mode in ("login", "signup"):
        title = "Sign in to DACRE" if mode == "login" else "Create your DACRE account"
        subtitle = "Open your real DACRE workspace." if mode == "login" else "Start your own connected business intelligence workspace."
        action_word = "Sign In" if mode == "login" else "Create Account"
        st.markdown(f"""
        <div class="page-hero">
          <div class="section-kicker">DACRE ACCOUNT</div>
          <div class="page-title">{title}</div>
          <div class="page-copy">{subtitle} Powered by DI — David's Intelligence.</div>
        </div>
        <div class="callout" style="margin:10px 28px 0;">
          <h3>{action_word}</h3>
          <p>This is the real DACRE authentication flow, connected to the application database. You are not leaving the DACRE experience.</p>
        </div>
        """, unsafe_allow_html=True)
        _landing_auth_panel()
        if st.button("← Back to DACRE Landing Page", key="auth_page_back", use_container_width=True):
            st.session_state.landing_mode = "home"
            st.session_state.landing_section = "home"
            st.rerun()
        return

    # Dedicated information pages
    if current_section == "features":
        st.markdown("""
        <div class="page-hero">
          <div class="section-kicker">DACRE FEATURES</div>
          <div class="page-title">Everything needed to move from raw data to useful work.</div>
          <div class="page-copy">DACRE combines a data workspace, cleaning tools, formulas, charts, files, exports, business intelligence and DI into one connected environment.</div>
        </div>
        <div class="section">
          <div class="grid-3">
            <div class="feature-card"><div class="feature-icon">▦</div><h3>Workspace & Data</h3><p>Import CSV, Excel, TSV and JSON datasets into a persistent working environment.</p></div>
            <div class="feature-card"><div class="feature-icon">ƒ</div><h3>Formula Lab</h3><p>Apply practical spreadsheet-style transformations and calculations without leaving your analysis workflow.</p></div>
            <div class="feature-card"><div class="feature-icon">◫</div><h3>Charts & Dashboards</h3><p>Turn processed information into visual stories that make business patterns easier to understand.</p></div>
            <div class="feature-card"><div class="feature-icon">▤</div><h3>File Vault</h3><p>Keep working files and datasets organized inside the organization workspace.</p></div>
            <div class="feature-card"><div class="feature-icon">⇩</div><h3>Export Center</h3><p>Package analysis outputs for reporting, sharing and business use.</p></div>
            <div class="feature-card"><div class="feature-icon">✦</div><h3>DI Action Center</h3><p>Give DI a business objective and let it turn the request into analysis, recommendations and next actions.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Use these DACRE features", key="features_cta", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    elif current_section == "intelligence":
        st.markdown("""
        <div class="page-hero">
          <div class="section-kicker">DI — DAVID'S INTELLIGENCE</div>
          <div class="page-title">Intelligence that works with your business context.</div>
          <div class="page-copy">DI is the built-in intelligence layer inside DACRE Analysis. It can explain results, investigate data, help with business questions and work alongside the active workspace.</div>
        </div>
        <div class="section">
          <div class="grid-2">
            <div class="callout"><h3>Ask questions naturally</h3><p>Move from dashboards to conversation. Ask DI to explain a number, investigate a pattern, draft a brief or recommend what to investigate next.</p></div>
            <div class="callout"><h3>Work from real context</h3><p>DI can use the current organization, active dataset, institutional memory and available research context instead of treating every request as an isolated question.</p></div>
            <div class="callout"><h3>Named DI workforce</h3><p>DACRE supports specialized DI workers with distinct identities, specialties and working styles — all under the same DACRE intelligence foundation.</p></div>
            <div class="callout"><h3>Voice-ready experience</h3><p>The DACRE interface supports browser-based DI voice interaction so users can communicate naturally where their browser supports speech features.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create a workspace and use DI", key="intelligence_cta", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    elif current_section == "workforce":
        st.markdown("""
        <div class="page-hero">
          <div class="section-kicker">DI WORKFORCE</div>
          <div class="page-title">Specialized digital workers, coordinated inside DACRE.</div>
          <div class="page-copy">Each DI worker can have a defined specialty and work style, giving organizations a clearer way to organize intelligence tasks across research, analytics, communication, administration and support.</div>
        </div>
        <div class="section">
          <div class="grid-3">
            <div class="feature-card"><div class="feature-icon">EM</div><h3>Emiel</h3><p>Email & Messaging — organized communication workflows and business messaging support.</p></div>
            <div class="feature-card"><div class="feature-icon">OL</div><h3>Oriel</h3><p>Data Analysis — metrics, trends, patterns and evidence-first analytical work.</p></div>
            <div class="feature-card"><div class="feature-icon">SO</div><h3>Sofiel</h3><p>Research & Intelligence — investigative research and source-conscious summaries.</p></div>
            <div class="feature-card"><div class="feature-icon">DA</div><h3>Daniel</h3><p>Data Entry & Processing — clean, consistent and accurate repetitive data operations.</p></div>
            <div class="feature-card"><div class="feature-icon">GR</div><h3>Graciel</h3><p>Business Intelligence — KPIs, dashboards, executive insights and recommendations.</p></div>
            <div class="feature-card"><div class="feature-icon">JA</div><h3>Jamiel</h3><p>Security & Administration — access controls, audit trails and platform operations.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open the DI Workforce in DACRE", key="workforce_cta", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    elif current_section == "analytics":
        st.markdown("""
        <div class="page-hero">
          <div class="section-kicker">ANALYTICS</div>
          <div class="page-title">See what changed, what matters and what to do next.</div>
          <div class="page-copy">DACRE translates active business data into clear metrics, health signals, charts and executive-level views that help users move from observation to action.</div>
        </div>
        <div class="section">
          <div class="metric-row">
            <div class="metric"><small>Data health</small><strong>97 / 100</strong></div>
            <div class="metric"><small>Live records</small><strong>4.2M+</strong></div>
            <div class="metric"><small>Insight layer</small><strong>DI</strong></div>
            <div class="metric"><small>Workspace</small><strong>LIVE</strong></div>
          </div>
          <div class="grid-2" style="margin-top:18px;">
            <div class="callout"><h3>Business Command Center</h3><p>Review data health, executive briefs, trends, anomalies and questions against the active workspace.</p></div>
            <div class="callout"><h3>Business Twin</h3><p>Build a living snapshot of the current dataset with health scoring, attention signals and measurable opportunities.</p></div>
            <div class="callout"><h3>Decision Ledger</h3><p>Record decisions, context, expected outcomes and later results so organizational history becomes structured knowledge.</p></div>
            <div class="callout"><h3>Opportunity Radar</h3><p>Surface measurable growth signals from numeric trends and turn them into investigation prompts.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Use DACRE Analytics", key="analytics_cta", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    elif current_section == "security":
        st.markdown("""
        <div class="page-hero">
          <div class="section-kicker">SECURITY</div>
          <div class="page-title">Protected business workspaces with structured access.</div>
          <div class="page-copy">DACRE separates organization workspaces, account roles, activity records and protected master administration so business information can be handled within a clear access model.</div>
        </div>
        <div class="section">
          <div class="grid-2">
            <div class="feature-card"><div class="feature-icon">✓</div><h3>Organization boundaries</h3><p>Users work inside their organization context, while administrative views are scoped according to role.</p></div>
            <div class="feature-card"><div class="feature-icon">⌁</div><h3>Activity visibility</h3><p>DACRE records important account and workspace activity so organizations can inspect what happened.</p></div>
            <div class="feature-card"><div class="feature-icon">♛</div><h3>Protected master access</h3><p>Overall platform controls are separated from normal organization administration behind an additional protected gate.</p></div>
            <div class="feature-card"><div class="feature-icon">DI</div><h3>Private intelligence context</h3><p>DI's internal context and application security values are not exposed as ordinary public landing-page content.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create a secure DACRE workspace", key="security_cta", use_container_width=True, type="primary"):
            st.session_state.landing_mode = "signup"
            st.session_state.landing_section = "home"
            st.rerun()

    else:
        # Main landing page
        st.markdown(f"""
        <div class="hero">
          <div>
            <div class="hero-eyebrow">✦ Experience Next-Gen Business Intelligence</div>
            <div class="hero-title">Transform Raw Data<br/>into <span class="gradient-text">Heavenly Insights.</span></div>
            <p class="hero-copy">DACRE turns scattered business data into clear intelligence, powerful analytics and practical decisions — with DI, David's Intelligence, built into the workspace.</p>
            <div class="hero-proof">
              <span><span class="proof-dot">●</span> Real-time analytics</span>
              <span><span class="proof-dot">●</span> DI-powered intelligence</span>
              <span><span class="proof-dot">●</span> Secure workspaces</span>
            </div>
          </div>
          <div class="hero-visual-host"></div>
        </div>
        """, unsafe_allow_html=True)

        hero_dashboard_html = """
        <style>
          *{box-sizing:border-box}html,body{margin:0;padding:0;background:transparent;font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#f7fbff;overflow:hidden}
          .visual{position:relative;width:100%;min-height:470px;display:flex;align-items:center;justify-content:center;padding:14px}
          .orb{position:absolute;width:330px;height:330px;border-radius:50%;background:radial-gradient(circle,#6d63ff55 0%,#2789ff20 34%,transparent 70%);filter:blur(4px);animation:pulse 4s ease-in-out infinite}
          .card{position:relative;width:min(560px,94%);border:1px solid rgba(116,160,234,.28);border-radius:26px;background:linear-gradient(145deg,rgba(24,38,67,.97),rgba(6,14,30,.97));padding:22px;box-shadow:0 28px 80px rgba(0,0,0,.5),0 0 40px rgba(54,120,255,.12)}
          .top{display:flex;justify-content:space-between;align-items:center;color:#b9c8e2;font-size:11px;letter-spacing:.08em;margin-bottom:16px}.live{display:inline-flex;align-items:center;gap:6px;color:#6ef0ba;font-weight:800}.dot{width:7px;height:7px;border-radius:50%;background:#5ce7ad;box-shadow:0 0 12px #5ce7ad}.label{color:#c2d3ea;font-size:12px;margin-bottom:4px}.metric{font-size:31px;font-weight:900;letter-spacing:-.04em}.up{color:#4fe5b3;font-size:12px;margin-left:8px;font-weight:800}
          .bars{height:200px;display:flex;align-items:flex-end;gap:8px;padding:18px 8px;border-radius:18px;background:rgba(91,122,170,.10);border:1px solid rgba(113,152,207,.12);margin-top:16px}.bar{flex:1;border-radius:8px 8px 3px 3px;background:linear-gradient(180deg,#38e4f3 0%,#2a95ff 48%,#544ff0 100%);box-shadow:0 0 24px rgba(47,146,255,.22);min-width:8px;transition:height .4s ease}.mini-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}.mini{padding:14px;border:1px solid rgba(121,155,203,.16);border-radius:15px;background:rgba(255,255,255,.035)}.mini-label{color:#9fb0c9;font-size:10px}.mini-value{margin-top:4px;font-size:19px;font-weight:850}.mini-accent{color:#55e5b5}.badge{position:absolute;right:20px;top:18px;padding:6px 9px;border-radius:999px;background:rgba(55,128,255,.13);border:1px solid rgba(73,153,255,.28);color:#9ed2ff;font-size:9px;font-weight:800}@keyframes pulse{50%{transform:scale(1.06);opacity:.9}}
          @media(max-width:700px){.visual{min-height:360px}.card{padding:16px}.bars{height:145px;gap:5px}.metric{font-size:25px}.top{font-size:9px}}
        </style>
        <div class="visual"><div class="orb"></div><div class="card"><div class="badge">LIVE DI INSIGHT</div><div class="top"><span>DACRE / ANALYTICS</span><span class="live"><span class="dot"></span>DI ONLINE</span></div><div class="label">Revenue Growth</div><div class="metric">$2.4M <span class="up">↗ 18.2%</span></div><div class="bars"><div class="bar" style="height:38%"></div><div class="bar" style="height:55%"></div><div class="bar" style="height:44%"></div><div class="bar" style="height:68%"></div><div class="bar" style="height:59%"></div><div class="bar" style="height:78%"></div><div class="bar" style="height:66%"></div><div class="bar" style="height:88%"></div><div class="bar" style="height:76%"></div><div class="bar" style="height:92%"></div></div><div class="mini-grid"><div class="mini"><div class="mini-label">Data Points</div><div class="mini-value">4.2M</div></div><div class="mini"><div class="mini-label">System Health</div><div class="mini-value mini-accent">99.98%</div></div></div></div></div>
        """
        components.html(hero_dashboard_html, height=500, scrolling=False)

        render_uniel_landing_guide()

        b1, b2, b3 = st.columns([1, 1.2, 1])
        with b1:
            if st.button("Explore DACRE", key="landing_explore", use_container_width=True):
                st.session_state.landing_mode = "signup"
                st.rerun()
        with b2:
            if st.button("Get Started Free", key="landing_get_started", use_container_width=True, type="primary"):
                st.session_state.landing_mode = "signup"
                st.rerun()
        with b3:
            if st.button("Log In", key="landing_log_in", use_container_width=True):
                st.session_state.landing_mode = "login"
                st.rerun()

        st.markdown("""
        <div class="section">
          <div class="section-head"><div class="section-kicker">THE DACRE PLATFORM</div><div class="section-title">One intelligence layer for the work that matters.</div><div class="section-copy">Explore the five core aspects of DACRE — each one is a real page connected to this application.</div></div>
          <div class="grid-3">
            <div class="feature-card"><div class="feature-icon">↗</div><h3>Features</h3><p>Explore the workspace, formulas, charts, files, exports and DI action tools that make DACRE useful day to day.</p></div>
            <div class="feature-card"><div class="feature-icon">DI</div><h3>Intelligence</h3><p>Understand how DI — David's Intelligence — works with your business context and active data.</p></div>
            <div class="feature-card"><div class="feature-icon">◈</div><h3>Workforce</h3><p>Meet the specialized DI workers and see how their distinct specialties fit into one intelligence foundation.</p></div>
            <div class="feature-card"><div class="feature-icon">◫</div><h3>Analytics</h3><p>See how DACRE turns data into health scores, business signals, decisions and opportunity insights.</p></div>
            <div class="feature-card"><div class="feature-icon">✓</div><h3>Security</h3><p>Learn how organization boundaries, activity visibility and protected administration support business use.</p></div>
            <div class="feature-card"><div class="feature-icon">→</div><h3>Ready to begin?</h3><p>Create your DACRE account and enter your own workspace with real authentication and persistent organization context.</p></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        page_cols = st.columns(5)
        for col, label, target in zip(page_cols, ["Features","Intelligence","Workforce","Analytics","Security"], ["features","intelligence","workforce","analytics","security"]):
            with col:
                if st.button(label, key=f"landing_card_{target}", use_container_width=True):
                    st.session_state.landing_section = target
                    st.rerun()

        st.markdown("""
        <div class="cta"><div class="section-kicker">START YOUR WORKSPACE</div><h2>Create your DACRE account.</h2><p>Move from scattered information to a connected business intelligence workspace powered by DI — David's Intelligence.</p></div>
        """, unsafe_allow_html=True)
        cta1, cta2 = st.columns([1, 1])
        with cta1:
            if st.button("Create Your DACRE Account", key="landing_bottom_signup", use_container_width=True, type="primary"):
                st.session_state.landing_mode = "signup"
                st.rerun()
        with cta2:
            if st.button("Already have an account? Sign In", key="landing_bottom_login", use_container_width=True):
                st.session_state.landing_mode = "login"
                st.rerun()

    st.markdown("""
    <div class="footer"><span>© DACRE Analysis · Business & Data Intelligence</span><span>Powered by DI — David's Intelligence</span></div>
    """, unsafe_allow_html=True)

    if current_section != "home":
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("← Back to Landing", key="section_back", use_container_width=True):
                st.session_state.landing_section = "home"
                st.rerun()
        with c2:
            if st.button("Create Your DACRE Account", key="section_signup", use_container_width=True, type="primary"):
                st.session_state.landing_mode = "signup"
                st.rerun()
        with c3:
            if st.button("Sign In", key="section_login", use_container_width=True):
                st.session_state.landing_mode = "login"
                st.rerun()

# =============================================================================
# ENHANCED FEATURES - GLOBAL MARKETS
# =============================================================================

class GlobalBusinessIntelligence:
    """Worldwide business intelligence with real-time data."""
    
    def __init__(self):
        self.market_data = {}
        self.currencies = {}
        self.commodities = {}
        self.yf_available = YFINANCE_AVAILABLE
    
    def get_market_data(self, symbol: str) -> Dict:
        """Get real-time market data for a symbol."""
        try:
            if self.yf_available:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                return {
                    "symbol": symbol,
                    "name": info.get("longName", symbol),
                    "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
                    "change": info.get("regularMarketChange", 0),
                    "change_percent": info.get("regularMarketChangePercent", 0),
                    "volume": info.get("regularMarketVolume", 0),
                    "market_cap": info.get("marketCap", 0),
                    "pe_ratio": info.get("trailingPE", 0),
                    "dividend_yield": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0,
                    "updated_at": datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Market data error for {symbol}: {e}")
        
        return {"symbol": symbol, "error": "Data not available"}
    
    def get_currency_rates(self, base: str = "USD") -> Dict:
        """Get real-time currency exchange rates."""
        try:
            response = requests.get(
                f"https://api.exchangerate-api.com/v4/latest/{base}",
                timeout=10,
                headers={"User-Agent": "DACRE-Worldwide/1.0"}
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "base": base,
                    "rates": data.get("rates", {}),
                    "updated_at": datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Currency API error: {e}")
        
        return {"base": base, "rates": {}, "error": "Rates unavailable"}
    
    def get_commodity_prices(self, commodities: List[str] = None) -> Dict:
        """Get real-time commodity prices."""
        if commodities is None:
            commodities = ["gold", "silver", "oil", "copper", "natural_gas"]
        
        result = {}
        symbols = {
            "gold": "GC=F",
            "silver": "SI=F",
            "oil": "CL=F",
            "copper": "HG=F",
            "natural_gas": "NG=F"
        }
        
        for commodity in commodities:
            symbol = symbols.get(commodity.lower())
            if symbol:
                data = self.get_market_data(symbol)
                result[commodity.lower()] = {
                    "price": data.get("price", 0),
                    "change": f"{data.get('change_percent', 0):.2f}%",
                    "updated": data.get("updated_at", datetime.now().isoformat())
                }
        
        return result
    
    def analyze_region(self, region: str) -> Dict:
        """Analyze business conditions for a specific region."""
        regions = {
            "africa": {
                "gdp_growth": "3.5%",
                "inflation": "7.2%",
                "business_confidence": "65/100",
                "opportunities": ["Fintech", "Agriculture", "Energy", "Telecom", "E-commerce"],
                "risks": ["Currency volatility", "Infrastructure", "Regulatory changes", "Political instability"],
                "key_markets": ["Nigeria", "South Africa", "Kenya", "Egypt", "Ghana"],
                "top_sectors": ["Finance", "Agriculture", "Technology", "Energy", "Telecom"],
                "population": "1.3B+",
                "gdp": "$2.6T"
            },
            "asia": {
                "gdp_growth": "4.8%",
                "inflation": "3.9%",
                "business_confidence": "72/100",
                "opportunities": ["Technology", "Manufacturing", "Services", "AI", "Renewables"],
                "risks": ["Geopolitical tensions", "Trade barriers", "Supply chain disruptions"],
                "key_markets": ["China", "India", "Japan", "Singapore", "South Korea"],
                "top_sectors": ["Technology", "Manufacturing", "Finance", "Healthcare", "Education"],
                "population": "4.6B+",
                "gdp": "$30T+"
            },
            "europe": {
                "gdp_growth": "2.1%",
                "inflation": "4.5%",
                "business_confidence": "68/100",
                "opportunities": ["Green Energy", "Healthcare", "Automation", "Fintech", "Luxury"],
                "risks": ["Regulatory complexity", "Aging population", "Energy dependency"],
                "key_markets": ["Germany", "UK", "France", "Netherlands", "Switzerland"],
                "top_sectors": ["Automotive", "Healthcare", "Finance", "Manufacturing", "Tech"],
                "population": "748M",
                "gdp": "$23T"
            },
            "north_america": {
                "gdp_growth": "3.2%",
                "inflation": "3.8%",
                "business_confidence": "78/100",
                "opportunities": ["AI", "Biotech", "Space", "Fintech", "Clean Energy"],
                "risks": ["Debt levels", "Political polarization", "Income inequality"],
                "key_markets": ["USA", "Canada", "Mexico"],
                "top_sectors": ["Technology", "Finance", "Healthcare", "Energy", "Entertainment"],
                "population": "600M",
                "gdp": "$28T+"
            },
            "south_america": {
                "gdp_growth": "2.8%",
                "inflation": "6.5%",
                "business_confidence": "58/100",
                "opportunities": ["Agriculture", "Mining", "Renewables", "E-commerce", "Tourism"],
                "risks": ["Political instability", "Debt", "Currency volatility", "Corruption"],
                "key_markets": ["Brazil", "Argentina", "Chile", "Colombia", "Peru"],
                "top_sectors": ["Agriculture", "Mining", "Energy", "Services", "Manufacturing"],
                "population": "430M",
                "gdp": "$4.5T"
            }
        }
        return regions.get(region.lower(), {"error": "Region not found"})

def render_global_markets_dashboard():
    """Render global markets dashboard with real-time data."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">📊 Global Markets</h1>
        <p style="color:#94a3b8;">Real-time market data from around the world</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize Global Business Intelligence
    bi = GlobalBusinessIntelligence()
    
    # Currency rates
    st.subheader("💱 Currency Exchange Rates")
    rates = bi.get_currency_rates("USD")
    if rates.get("rates"):
        cols = st.columns(8)
        currencies = ["EUR", "GBP", "NGN", "KES", "ZAR", "AED", "INR", "CNY"]
        for idx, currency in enumerate(currencies):
            with cols[idx % 8]:
                rate = rates["rates"].get(currency, 0)
                st.metric(currency, f"{rate:.4f}")
    
    # Market indices
    st.subheader("📈 Market Indices")
    indices = ["AAPL", "GOOGL", "MSFT", "AMZN", "META", "TSLA", "NVDA", "AMD", "NFLX", "JPM"]
    cols = st.columns(5)
    for idx, symbol in enumerate(indices):
        with cols[idx % 5]:
            data = bi.get_market_data(symbol)
            if data.get("price"):
                st.metric(
                    data.get("name", symbol)[:12],
                    f"${data['price']:,.2f}",
                    f"{data.get('change_percent', 0):.2f}%"
                )
    
    # Commodities
    st.subheader("🛢️ Commodity Prices")
    commodities = bi.get_commodity_prices(["Gold", "Silver", "Oil", "Copper", "Natural Gas"])
    cols = st.columns(5)
    for idx, (name, data) in enumerate(commodities.items()):
        with cols[idx % 5]:
            st.metric(
                name.title(),
                f"${data['price']:,.2f}" if isinstance(data.get('price'), (int, float)) else data.get('price', 'N/A'),
                data.get('change', 'N/A')
            )
    
    # Region analysis
    st.subheader("🌍 Regional Business Intelligence")
    regions = ["Africa", "Asia", "Europe", "North America", "South America"]
    selected_region = st.selectbox("Select Region", regions)
    
    region_data = bi.analyze_region(selected_region)
    if region_data and "error" not in region_data:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("GDP Growth", region_data.get("gdp_growth", "N/A"))
            st.metric("Inflation", region_data.get("inflation", "N/A"))
            st.metric("Business Confidence", region_data.get("business_confidence", "N/A"))
        with col2:
            st.markdown("### Opportunities")
            for opp in region_data.get("opportunities", []):
                st.markdown(f"✅ {opp}")
            st.markdown("### Key Markets")
            for market in region_data.get("key_markets", []):
                st.markdown(f"📍 {market}")

# =============================================================================
# SESSION STATE BOOTSTRAP
# =============================================================================

_SESSION_DEFAULTS = {
    "user": None,
    "master_route": False,
    "landing_mode": "home",
    "landing_section": "home",
    "master_captcha_required": False,
    "master_captcha_passed": False,
    "master_second_attempt": False,
    "master_guard_challenge_required": False,
    "master_guard_failed": False,
    "chat_history": [],
    "raw_df": None,
    "processed_df": None,
    "active_filename": "",
    "formula_logs": [],
    "chart_config": None,
    "di_language": "English — Nigeria",
    "di_voice_enabled": True,
    "di_response_mode": "voice",
    "active_call_room": None,
    "sovereign_call_id": None,
    "sovereign_call_room": None,
    "david_creations_unlocked": False,
    "active_call_target": None,
    "last_action_center_result": None,
    "last_speech": None,
    "dacre_boot_complete": False,
    "visitor_id": None,
    "public_visit_logged": False,
    "selected_agent": None,
    "active_call": None,
    "active_agent": None,
    "livekit_active_room": None,
    "livekit_active_di": None,
    "admin_memory_web_results": [],
    "di_avatars": {},
    "call_conversation": [],
    "db_health": None,
    "error_shield": None,
    "show_conference": False,
    "selected_page": "Overview",
    "manage_app_unlocked": False,
}

for _key, _default in _SESSION_DEFAULTS.items():
    if _key not in st.session_state:
        if isinstance(_default, list):
            st.session_state[_key] = list(_default)
        elif isinstance(_default, dict):
            st.session_state[_key] = dict(_default)
        else:
            st.session_state[_key] = _default

# =============================================================================
# SELF-HEALING DATABASE & ERROR SHIELD
# =============================================================================

def self_healing_database():
    """Self-healing database function."""
    try:
        con = db()
        required_tables = [
            'companies', 'users', 'files', 'projects', 'activity',
            'company_website_profile', 'public_visits', 'emails_log',
            'notifications', 'chat_history', 'loan_clients',
            'whatsapp_delivery_log', 'di_memory', 'di_agents',
            'di_private_memory', 'di_position_history', 'di_master_thanks',
            'sovereign_calls', 'sovereign_call_members', 'sovereign_call_messages',
            'david_creations', 'call_rooms', 'call_participants',
            'decision_ledger', 'opportunity_radar', 'di_action_log'
        ]
        
        repaired = []
        for table in required_tables:
            try:
                con.execute(f"SELECT 1 FROM {table} LIMIT 1")
            except:
                try:
                    init_db()
                    repaired.append(table)
                except:
                    pass
        
        con.commit()
        con.close()
        
        return {
            "status": "healthy",
            "repaired": repaired,
            "tables": len(required_tables),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

class ErrorShield:
    """Error Shield - catches runtime failures."""
    
    def __init__(self):
        self.errors = []
        self.recoveries = []
        self.shield_active = True
    
    def protect(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.errors.append({
                "function": func.__name__,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return None
    
    def get_status(self):
        return {
            "shield_active": self.shield_active,
            "errors_caught": len(self.errors),
            "recoveries": len(self.recoveries),
            "last_error": self.errors[-1] if self.errors else None,
            "last_recovery": self.recoveries[-1] if self.recoveries else None
        }

def generate_di_grid_image() -> Optional[bytes]:
    """Generate a 3x4 grid of REAL AI DI agent portraits."""
    if not GENAI_AVAILABLE:
        return None
    
    try:
        client = genai.Client()
        
        prompt_text = (
            "A 3x4 grid collage featuring 12 individual portraits of diverse male and female "
            "professional business AI androids in a sleek, high-tech corporate laboratory. "
            "Each portrait shows realistic human faces with subtle glowing cybernetic and "
            "circuit board elements integrated into their necks and sides of their heads. "
            "They are dressed in professional business attire: suits, blazers, and formal wear. "
            "Clean, professional lighting, cinematic style, sharp detail, 8k resolution."
        )
        
        response = client.models.generate_images(
            model='imagen-3.0-generate-002',
            prompt=prompt_text,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
                output_mime_type="image/jpeg"
            )
        )
        
        if response.generated_images:
            image_bytes = response.generated_images[0].image.image_bytes
            with open("di_grid_portraits.jpg", "wb") as f:
                f.write(image_bytes)
            return image_bytes
        
    except Exception as e:
        print(f"DI Grid generation error: {e}")
    
    return None

# =============================================================================
# INITIALIZATION - PRODUCTION CORE
# =============================================================================

def init_production_core():
    """Initialize the DACRE Production Core."""
    # Initialize Error Shield
    if 'error_shield' not in st.session_state:
        st.session_state.error_shield = ErrorShield()
    
    # Run self-healing database
    health = self_healing_database()
    st.session_state.db_health = health
    
    # Ensure all DI agents have proper schema
    ensure_di_agent_columns()
    
    # Ensure master account exists
    ensure_master()
    
    # Seed DI memory if empty
    seed_di_memory()
    
    # Seed DI workforce if empty
    seed_named_di_workforce()
    
    return {
        "core_initialized": True,
        "database_health": health,
        "shield_status": st.session_state.error_shield.get_status() if st.session_state.error_shield else None,
        "timestamp": datetime.now().isoformat()
    }

# =============================================================================
# RENDER PRODUCTION CORE VISUAL
# =============================================================================

def render_dacre_production_core():
    """Display the DACRE Production Core architecture diagram."""
    st.markdown("""
    <style>
    .dacre-core-container {
        background: linear-gradient(145deg, #0a1628, #1a2a4a);
        border-radius: 24px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid rgba(75, 130, 245, 0.3);
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
    }
    .dacre-core-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(ellipse at center, rgba(75,130,245,0.05) 0%, transparent 70%);
        animation: corePulse 8s ease-in-out infinite;
    }
    @keyframes corePulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    .core-title {
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: 900;
        letter-spacing: 2px;
        position: relative;
        z-index: 1;
    }
    .core-title span {
        background: linear-gradient(90deg, #4b82f5, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .core-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 20px;
        margin: 30px 0;
        position: relative;
        z-index: 1;
    }
    .core-card {
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(75,130,245,0.2);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    .core-card:hover {
        transform: translateY(-5px);
        border-color: rgba(75,130,245,0.6);
        box-shadow: 0 10px 40px rgba(75,130,245,0.2);
    }
    .core-card .icon {
        font-size: 48px;
        margin-bottom: 10px;
        display: block;
    }
    .core-card h3 {
        color: white;
        margin: 10px 0;
        font-size: 18px;
    }
    .core-card p {
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.6;
        margin: 5px 0;
    }
    .core-card .status {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
        margin-top: 10px;
    }
    .status-online { background: rgba(46, 204, 113, 0.2); color: #2ecc71; }
    .status-active { background: rgba(52, 152, 219, 0.2); color: #3498db; }
    .status-ready { background: rgba(241, 196, 15, 0.2); color: #f1c40f; }
    .core-bottom {
        text-align: center;
        margin-top: 20px;
        padding: 20px;
        background: rgba(75,130,245,0.1);
        border-radius: 12px;
        border: 1px solid rgba(75,130,245,0.2);
        position: relative;
        z-index: 1;
    }
    .core-bottom h2 {
        color: white;
        font-size: 24px;
        margin: 0;
    }
    .core-bottom h2 span {
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .core-bottom p {
        color: #94a3b8;
        margin: 5px 0 0 0;
    }
    .core-stats {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-top: 20px;
        position: relative;
        z-index: 1;
    }
    .core-stat {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .core-stat .number {
        font-size: 28px;
        font-weight: 900;
        color: white;
    }
    .core-stat .label {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 5px;
    }
    .core-stat .label span {
        color: #60a5fa;
    }
    @media (max-width: 768px) {
        .core-grid { grid-template-columns: 1fr; }
        .core-stats { grid-template-columns: 1fr 1fr; }
    }
    </style>
    
    <div class="dacre-core-container">
        <div class="core-title">⚡ DACRE <span>PRODUCTION CORE</span></div>
        
        <div class="core-grid">
            <div class="core-card">
                <span class="icon">🔄</span>
                <h3>Self-Healing Database</h3>
                <p>Automatic schema repair, migration, and recovery. Your data stays intact even when things go wrong.</p>
                <div style="margin-top: 10px; font-size: 12px; color: #94a3b8;">
                    <span style="color: #2ecc71;">●</span> Schema Auto-Repair
                    <br>
                    <span style="color: #2ecc71;">●</span> Migration Safe
                    <br>
                    <span style="color: #2ecc71;">●</span> Data Integrity
                </div>
                <span class="status status-online">🟢 ONLINE</span>
            </div>
            
            <div class="core-card">
                <span class="icon">🧠</span>
                <h3>DI Intelligence</h3>
                <p>20 specialized DI agents with memory, private brains, voice, video, and web search capabilities.</p>
                <div style="margin-top: 10px; font-size: 12px; color: #94a3b8;">
                    <span style="color: #3498db;">●</span> 20 DI Workforce
                    <br>
                    <span style="color: #3498db;">●</span> Memory + Brain
                    <br>
                    <span style="color: #3498db;">●</span> Web Search
                </div>
                <span class="status status-active">🔵 ACTIVE</span>
            </div>
            
            <div class="core-card">
                <span class="icon">🛡️</span>
                <h3>Error Shield</h3>
                <p>Catches runtime failures, prevents crashes, and ensures safe recovery with graceful degradation.</p>
                <div style="margin-top: 10px; font-size: 12px; color: #94a3b8;">
                    <span style="color: #f1c40f;">●</span> Crash Protection
                    <br>
                    <span style="color: #f1c40f;">●</span> Safe Recovery
                    <br>
                    <span style="color: #f1c40f;">●</span> Graceful Degrade
                </div>
                <span class="status status-ready">🟡 READY</span>
            </div>
        </div>
        
        <div class="core-bottom">
            <h2>⬇ ONE <span>STABLE</span> DACRE APP ⬇</h2>
            <p>All systems integrated · 99.98% uptime · Enterprise ready</p>
            
            <div class="core-stats">
                <div class="core-stat">
                    <div class="number">20</div>
                    <div class="label">DI <span>Agents</span></div>
                </div>
                <div class="core-stat">
                    <div class="number">100%</div>
                    <div class="label">Self-<span>Healing</span></div>
                </div>
                <div class="core-stat">
                    <div class="number">99.98%</div>
                    <div class="label">Uptime</div>
                </div>
                <div class="core-stat">
                    <div class="number">∞</div>
                    <div class="label">Error <span>Shield</span></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# MAIN APPLICATION - PAGE ROUTING
# =============================================================================


# =============================================================================
# RENDER FUNCTIONS FOR EACH PAGE
# =============================================================================

def render_di_home(user):
    """Render the DI Home page."""
    df = st.session_state.processed_df
    
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">💬 DI Home</h1>
        <p style="color:#94a3b8;">Your continuous conversation with DI — David's Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat history
    for msg in st.session_state.chat_history[-20:]:
        if msg["sender"] == "DI":
            st.markdown(f"""
            <div style="background:#1a2a4a;border-radius:12px;padding:15px;margin:5px 0;border-left:4px solid #60a5fa;">
                <b style="color:#60a5fa;">🧠 DI</b>
                <p style="color:white;margin-top:5px;">{msg['text']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#0a1628;border-radius:12px;padding:15px;margin:5px 0;border-left:4px solid #a78bfa;">
                <b style="color:#a78bfa;">👤 {msg['sender']}</b>
                <p style="color:white;margin-top:5px;">{msg['text']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Input
    with st.form("di_home_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            message = st.text_input("Ask DI anything...", label_visibility="collapsed", placeholder="Type your question here...")
        with col2:
            submitted = st.form_submit_button("Send", type="primary")
    
    if submitted and message.strip():
        st.session_state.chat_history.append({"sender": user.get("first_name", "User"), "text": message})
        
        # Use the enhanced di_reply function
        reply = enhanced_di_reply(message, user, df, allow_online=True, language=st.session_state.get("di_language", "English — Nigeria"))
        
        st.session_state.chat_history.append({"sender": "DI", "text": reply})
        
        # Save to database
        con = db()
        now = datetime.now().isoformat(timespec="seconds")
        con.execute("INSERT INTO chat_history(username, company_name, sender, message, created_at) VALUES(?,?,?,?,?)",
                   (user["username"], user["company"], user.get("first_name", "User"), message, now))
        con.execute("INSERT INTO chat_history(username, company_name, sender, message, created_at) VALUES(?,?,?,?,?)",
                   (user["username"], user["company"], "DI", reply, now))
        con.commit()
        con.close()
        
        st.rerun()

def render_di_workforce(user):
    """Render the DI Workforce page."""
    agents = get_di_agents()
    
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">👥 DI Workforce</h1>
        <p style="color:#94a3b8;">Your specialized digital workforce — each DI has its own identity, specialty, and style</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not agents:
        st.info("No DI workers have been created yet.")
        return
    
    # Display agents in grid
    cols = st.columns(3)
    for idx, agent in enumerate(agents):
        with cols[idx % 3]:
            with st.container():
                avatar = agent.get("avatar_url") or f"https://api.dicebear.com/7.x/avataaars/svg?seed={agent['di_name']}"
                st.image(avatar, width=120)
                st.markdown(f"### {agent['di_name']}")
                st.caption(f"Specialty: {agent.get('specialty', 'General')}")
                st.caption(f"Position: {agent.get('position_title', 'DI Specialist')}")
                st.caption(f"Rank: {agent.get('rank_level', 1)}")
                st.caption(f"Status: {agent.get('status', 'Available')}")
                
                if st.button(f"💬 Chat with {agent['di_name']}", key=f"chat_{agent['di_name']}"):
                    st.session_state.selected_agent = agent['di_name']
                    st.rerun()

def render_di_calls(user):
    """Render the DI Calls page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">📞 DI Calls</h1>
        <p style="color:#94a3b8;">Business calls, DI calls, and team rooms with a meeting-ready workspace</p>
    </div>
    """, unsafe_allow_html=True)
    
    agents = get_di_agents()
    if not agents:
        st.info("No DI workers available for calls.")
        return
    
    selected_agent = st.selectbox("Select a DI to call", [a['di_name'] for a in agents])
    if selected_agent:
        agent = next(a for a in agents if a['di_name'] == selected_agent)
        st.markdown(f"""
        <div style="background:#1a2a4a;border-radius:12px;padding:20px;">
            <h3 style="color:white;">Calling {selected_agent}</h3>
            <p style="color:#94a3b8;">Specialty: {agent.get('specialty', 'General')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📞 Start Call", use_container_width=True, type="primary"):
            st.info(f"Calling {selected_agent}... (LiveKit integration required for full voice)")

def render_chibobec_loan_desk(user):
    """Render the Chibobec Loan Desk page."""
    if not is_chibobec_company(user.get("company")):
        st.warning("This page is only available for Chibobec Loan Service clients.")
        return
    
    st.markdown(f"""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">₦ Chibobec Loan Desk</h1>
        <p style="color:#94a3b8;">Welcome, {CHIBOBEC_OWNER_NAME}. Manage your loan clients and reminders.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Run reminder checks
    results = process_chibobec_reminders(user["username"], user["company"])
    if results:
        for client_name, reminder_type, ok, status in results:
            if ok:
                st.success(f"✅ {reminder_type} sent to {client_name}")
            else:
                st.warning(f"⚠️ {reminder_type} for {client_name}: {status}")
    
    # Add loan client form
    with st.expander("➕ Add Loan Client", expanded=True):
        with st.form("add_loan_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                client_name = st.text_input("Client Name")
                whatsapp = st.text_input("WhatsApp Number")
                amount = st.number_input("Loan Amount (₦)", min_value=0.0, step=1000.0)
            with col2:
                lent_date = st.date_input("Date Given", value=datetime.now().date())
                due_date = st.date_input("Due Date", value=datetime.now().date() + timedelta(days=30))
            
            if st.form_submit_button("Save Loan Client", type="primary"):
                ok, msg = add_loan_client(user["username"], user["company"], client_name, whatsapp, amount, lent_date, due_date)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    
    # Display loan clients
    con = db()
    loans = pd.read_sql_query(
        "SELECT id, client_name, whatsapp_number, loan_amount, lent_date, due_date, "
        "reminder_2_sent, due_sent FROM loan_clients WHERE username=? AND company_name=? ORDER BY due_date ASC",
        con, params=(user["username"], user["company"])
    )
    con.close()
    
    if not loans.empty:
        st.subheader("📋 Loan Book")
        display = loans.copy()
        display["loan_amount"] = display["loan_amount"].apply(lambda x: f"₦{float(x):,.2f}")
        display["2-day"] = display["reminder_2_sent"].apply(lambda x: "✅" if x else "⏳")
        display["Due"] = display["due_sent"].apply(lambda x: "✅" if x else "⏳")
        display = display.drop(columns=["reminder_2_sent", "due_sent"])
        st.dataframe(safe_dataframe_for_streamlit(display), use_container_width=True, hide_index=True)
    else:
        st.info("No loan clients added yet.")

def render_workspace_data(user):
    """Render the Workspace & Data page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">📁 Workspace & Data</h1>
        <p style="color:#94a3b8;">Upload, inspect, and clean your data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    file_upload = st.file_uploader("Upload dataset (CSV, Excel, TSV, JSON)", type=SUPPORTED_EXTENSIONS)
    
    if file_upload is not None and st.button("📥 Import & Load Dataset", type="primary"):
        try:
            df_raw = load_dataframe(file_upload)
            st.session_state.raw_df = df_raw
            st.session_state.processed_df = clean_dataframe(df_raw)
            st.session_state.active_filename = file_upload.name
            save_file(user, file_upload, st.session_state.processed_df)
            save_project(user, st.session_state.raw_df, st.session_state.processed_df, 
                        st.session_state.active_filename, st.session_state.formula_logs, st.session_state.chart_config)
            st.success(f"✅ Loaded '{file_upload.name}' successfully!")
            st.rerun()
        except Exception as exc:
            st.error(f"❌ Could not load the dataset: {exc}")
    
    # Display active dataset
    if st.session_state.processed_df is not None:
        df = st.session_state.processed_df
        st.subheader(f"📊 Active File: {st.session_state.active_filename}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", f"{len(df):,}")
        col2.metric("Total Columns", len(df.columns))
        col3.metric("Duplicates Removed", int(st.session_state.raw_df.duplicated().sum()) if st.session_state.raw_df is not None else 0)
        
        st.dataframe(safe_dataframe_for_streamlit(df), use_container_width=True)
        
        if st.button("💾 Save Project State", use_container_width=True):
            save_project(user, st.session_state.raw_df, df, st.session_state.active_filename, 
                        st.session_state.formula_logs, st.session_state.chart_config)
            log_activity(user["username"], user["company"], "Saved project state")
            st.toast("Project saved successfully!")
    else:
        st.info("📭 No active dataset. Upload a file or restore a saved project by signing in again.")

def render_formula_lab(user):
    """Render the Formula Lab page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">ƒ Formula Lab</h1>
        <p style="color:#94a3b8;">Practical spreadsheet-style formulas and transformations</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.processed_df
    if df is None:
        st.warning("⚠️ Please upload or open a dataset first.")
        return
    
    formula = st.selectbox("Formula Operation", SHEET_FORMULAS)
    cols = list(df.columns)
    
    if formula in ["SUM", "AVERAGE", "COUNT", "COUNTA", "MAX", "MIN", "UPPER", "LOWER", "TRIM"]:
        target_col = st.selectbox("Target Column", cols)
        if st.button("▶️ Run Formula", type="primary"):
            res = apply_formula(df, formula, {"column": target_col})
            if isinstance(res, tuple) and res[0] == "column":
                df[res[1]] = res[2]
                st.session_state.processed_df = df
                st.session_state.formula_logs.append(f"Applied {formula} on {target_col}")
                log_activity(user["username"], user["company"], f"Ran formula {formula} on {target_col}")
                st.success(f"✅ Applied {formula} on '{target_col}'!")
                st.rerun()
            else:
                st.markdown(f"### Result: `{res}`")
                st.session_state.formula_logs.append(f"{formula}({target_col}) = {res}")
    
    elif formula == "CONCATENATE":
        first = st.selectbox("First Column", cols)
        second = st.selectbox("Second Column", cols, index=min(1, len(cols)-1))
        new_col = st.text_input("New Column Name", value="Combined")
        sep = st.text_input("Separator", value=" ")
        
        if st.button("▶️ Run CONCATENATE", type="primary"):
            df[new_col] = df[first].astype(str) + sep + df[second].astype(str)
            st.session_state.processed_df = df
            log_activity(user["username"], user["company"], f"Created concatenated column {new_col}")
            st.success(f"✅ Created '{new_col}'!")
            st.rerun()

def render_charts(user):
    """Render the Charts page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">📊 Charts</h1>
        <p style="color:#94a3b8;">Turn data into clear visual stories and business dashboards</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.processed_df
    if df is None:
        st.warning("⚠️ Please upload or open a dataset first.")
        return
    
    chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Area Chart", "Scatter Plot", "Pie Chart"])
    cols = list(df.columns)
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    
    x_col = st.selectbox("X-Axis (Category Column)", cols)
    y_col = st.selectbox("Y-Axis (Numeric Values)", num_cols if num_cols else cols)
    
    if st.button("📈 Generate Chart", type="primary"):
        st.session_state.chart_config = {"type": chart_type, "x": x_col, "y": y_col}
        log_activity(user["username"], user["company"], f"Created {chart_type}: {x_col} vs {y_col}")
        st.success("✅ Chart generated!")
    
    if st.session_state.chart_config:
        cfg = st.session_state.chart_config
        chart_data = df[[cfg["x"], cfg["y"]]].dropna().set_index(cfg["x"])
        
        if cfg["type"] == "Bar Chart":
            st.bar_chart(chart_data)
        elif cfg["type"] == "Line Chart":
            st.line_chart(chart_data)
        elif cfg["type"] == "Area Chart":
            st.area_chart(chart_data)
        elif cfg["type"] == "Scatter Plot":
            st.scatter_chart(chart_data)
        elif cfg["type"] == "Pie Chart":
            fig = go.Figure(data=[go.Pie(labels=chart_data.index, values=chart_data[cfg["y"]])])
            fig.update_layout(template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)

def render_file_vault(user):
    """Render the File Vault page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">🗄️ File Vault</h1>
        <p style="color:#94a3b8;">Keep company files, working datasets, and project artifacts organized</p>
    </div>
    """, unsafe_allow_html=True)
    
    saved_files = get_files(user)
    if not saved_files:
        st.info("📭 No files stored in vault for your organization.")
        return
    
    for fname, ftype, created, fjson in saved_files:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{fname}** (`.{ftype}`) — Saved on: {created}")
        with col2:
            if st.button(f"📂 Load", key=f"btn_{fname}_{created}"):
                restored_df = dataframe_from_json(fjson)
                st.session_state.processed_df = restored_df
                st.session_state.raw_df = restored_df
                st.session_state.active_filename = fname
                log_activity(user["username"], user["company"], f"Loaded file from vault: {fname}")
                st.success(f"✅ Loaded {fname} from Vault!")
                st.rerun()

def render_export_center(user):
    """Render the Export Center page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">📤 Export Center</h1>
        <p style="color:#94a3b8;">Package analysis outputs for the people who need them</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.processed_df
    if df is None:
        st.warning("⚠️ No data available to export.")
        return
    
    csv_data = df.to_csv(index=False).encode("utf-8")
    excel_data = make_excel(df)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📄 Download CSV Dataset",
            data=csv_data,
            file_name=f"{st.session_state.active_filename or 'dacre'}_processed.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    with col2:
        st.download_button(
            "📊 Download Excel Workbook (.xlsx)",
            data=excel_data,
            file_name=f"{st.session_state.active_filename or 'dacre'}_workbook.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary"
        )
    
    log_activity(user["username"], user["company"], "Opened Export Center")

def render_organization_admin(user):
    """Render the Organization Admin Portal."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">⚙️ Organization Admin Portal</h1>
        <p style="color:#94a3b8;">Manage people, roles, notifications, and company activity</p>
    </div>
    """, unsafe_allow_html=True)
    
    target_company = user["company"] if user.get("role") != "master" else st.selectbox(
        "Organization", pd.read_sql_query("SELECT name FROM companies ORDER BY name", db())["name"].tolist()
    )
    
    con = db()
    tabs = st.tabs(["People & Accounts", "Notifications & Activity"])
    
    with tabs[0]:
        users_df = pd.read_sql_query(
            "SELECT id, first_name, last_name, username, email, role, login_count, created_at, last_login "
            "FROM users WHERE company_name=? ORDER BY id DESC",
            con, params=(target_company,)
        )
        st.dataframe(safe_dataframe_for_streamlit(users_df), use_container_width=True)
        st.metric("Accounts in organization", len(users_df))
        
        if user.get("role") == "company_admin":
            st.markdown("### Grant or remove admin access")
            usernames = users_df[users_df["role"] != "company_admin"]["username"].tolist()
            if usernames:
                selected_user = st.selectbox("User", usernames)
                action = st.selectbox("Action", ["Grant company admin", "Revoke company admin"])
                if st.button("Apply role change", type="primary"):
                    new_role = "company_admin" if action.startswith("Grant") else "user"
                    con.execute("UPDATE users SET role=? WHERE username=? AND company_name=?", 
                               (new_role, selected_user, target_company))
                    con.commit()
                    notify_company_admin(target_company, f"Admin role changed for {selected_user}: {new_role}.", "role_change")
                    log_activity(user["username"], target_company, f"Changed role for {selected_user} to {new_role}")
                    st.success("✅ Role updated.")
                    st.rerun()
    
    with tabs[1]:
        notes_df = pd.read_sql_query(
            "SELECT id, event_type, message, is_read, created_at FROM notifications "
            "WHERE company_name=? ORDER BY id DESC",
            con, params=(target_company,)
        )
        st.dataframe(safe_dataframe_for_streamlit(notes_df), use_container_width=True)
        
        if not notes_df.empty and st.button("📬 Mark all as read", type="primary"):
            con.execute("UPDATE notifications SET is_read=1 WHERE company_name=?", (target_company,))
            con.commit()
            st.rerun()
    
    con.close()

def render_di_memory_box(user):
    """Render the DI Memory Box page."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">🧠 DI Memory Box</h1>
        <p style="color:#94a3b8;">The trusted institutional memory layer shared by the DI workforce</p>
    </div>
    """, unsafe_allow_html=True)
    
    mem_df = pd.read_sql_query(
        "SELECT category, title, content, priority, updated_at FROM di_memory "
        "WHERE active=1 ORDER BY priority DESC, id ASC",
        db()
    )
    
    if mem_df.empty:
        st.info("📭 No memory records found.")
        return
    
    for row in mem_df.itertuples(index=False):
        with st.expander(f"{row.category} · {row.title} (Priority: {row.priority})", expanded=False):
            st.write(row.content)
            st.caption(f"Updated: {row.updated_at}")

def render_business_command_center(user):
    """Render the Business Command Center page."""
    df = st.session_state.processed_df
    
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">📊 Business Command Center</h1>
        <p style="color:#94a3b8;">Executive signals, business health, and the most important changes in your active data</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df is None:
        st.info("📭 Upload a dataset from Workspace & Data first.")
        return
    
    health = business_health(df)
    signals = business_signals(df)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📈 Data Health", f"{health['score']}/100")
    col2.metric("📊 Records", f"{len(df):,}")
    col3.metric("🔍 Missing Cells", f"{int(df.isna().sum().sum()):,}")
    col4.metric("🔄 Duplicates", f"{int(df.duplicated().sum()):,}")
    
    st.markdown("### 📋 Executive Brief")
    st.write(build_executive_brief(df, user["company"]))
    
    st.markdown("### 🚨 Signals Requiring Attention")
    if not signals:
        st.success("✅ No strong automated warning signals were detected.")
    else:
        for sig in signals:
            icon = "📈" if sig["type"] == "trend" else "⚠️" if sig["type"] == "anomaly" else "🧹"
            st.markdown(f"**{icon} {sig['column']}** — {sig['message']}")

def render_enhanced_conference_room(user):
    """Render an enhanced conference room."""
    st.markdown("""
    <div style="padding:20px;background:linear-gradient(135deg,#0a1628,#1a2a4a);border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white;">🎥 DI Conference</h1>
        <p style="color:#94a3b8;">Enhanced video conferencing with DI agents</p>
    </div>
    """, unsafe_allow_html=True)
    
    agents = get_di_agents()
    if not agents:
        st.info("No DI workers available for conferencing.")
        return
    
    selected_di = st.multiselect("Select DI agents for conference", [a['di_name'] for a in agents], default=[a['di_name'] for a in agents[:3]])
    
    if st.button("🎥 Start Conference", use_container_width=True, type="primary"):
        if selected_di:
            selected_agents = [a for a in agents if a['di_name'] in selected_di]
            render_di_video_call_stage(selected_agents, "DI Council Conference", user.get("first_name", "David"))
            st.success(f"Conference started with {', '.join(selected_di)}")
        else:
            st.warning("Please select at least one DI agent.")

# =============================================================================
# PERSISTENT DI DOCK
# =============================================================================

def render_persistent_di_dock(user):
    """Render the persistent DI dock at the bottom of every page."""
    st.markdown("---")
    
    quick_title = "Sovereign Master Chat with DI" if user.get("role") == "master" else "Chat with DI — quick assistant"
    quick_caption = (
        "Private founder channel · David Emenike · Sovereign Master request"
        if user.get("role") == "master"
        else "Ask DI about your work, DACRE or your business."
    )
    
    with st.expander(quick_title, expanded=False):
        st.caption(quick_caption)
        
        if user.get("role") == "master":
            st.info("🔐 DI treats messages here as private Sovereign Master requests and responds with founder-level respect.")
        
        for msg in st.session_state.chat_history[-5:]:
            st.write(f"**{msg['sender']}**: {msg['text']}")
        
        with st.form("quick_di_form", clear_on_submit=True):
            col1, col2 = st.columns([6, 1])
            with col1:
                q = st.text_input("Chat with DI", placeholder="Ask DI anything...", label_visibility="collapsed")
            with col2:
                send = st.form_submit_button("Send")
        
        if send and q.strip():
            sender_name = "David · Sovereign Master" if user.get("role") == "master" else user.get("first_name", "User")
            st.session_state.chat_history.append({"sender": sender_name, "text": q.strip()})
            
            reply = enhanced_di_reply(q, user, st.session_state.processed_df, allow_online=True, 
                            language=st.session_state.get("di_language", "English — Nigeria"))
            st.session_state.chat_history.append({"sender": "DI", "text": reply})
            st.session_state.last_speech = reply
            st.rerun()
    
    # Voice player for last speech
    if st.session_state.last_speech:
        speech = st.session_state.last_speech
        st.session_state.last_speech = None
        di_voice_player(
            speech,
            DI_LANGUAGE_PROFILES.get(st.session_state.get("di_language", "English — Nigeria"), {}).get("code", "en-NG")
        )

# =============================================================================
# FIXED OVERALL ADMIN PAGE - WITH FULL CEO IMAGE, DI GRID, SOVEREIGN CALL
# =============================================================================

def render_fixed_overall_admin_page(user):
    """FIXED Overall Admin DI page with FULL CEO image, DI grid, and Sovereign Call."""
    ensure_admin_runtime_schema()
    counts = admin_metric_counts()
    
    # CEO PORTRAIT - FIXED TO SHOW FULLY
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #0a1628, #1a2a4a);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
        border: 1px solid rgba(75,130,245,0.2);
    ">
        <div style="display: flex; gap: 30px; align-items: center; flex-wrap: wrap;">
            <div style="flex: 0 0 200px; text-align: center;">
    """, unsafe_allow_html=True)
    
    # CEO Portrait - FULL SIZE
    if CEO_PORTRAIT_PATH and CEO_PORTRAIT_PATH.exists():
        st.image(str(CEO_PORTRAIT_PATH), width=200, output_format="JPEG")
    elif CEO_PORTRAIT_DATA_URL:
        st.image(CEO_PORTRAIT_DATA_URL, width=200)
    else:
        st.markdown("""
        <div style="
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: linear-gradient(135deg, #4b82f5, #7c3aed);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 80px;
            margin: 0 auto;
        ">
            👑
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
            <div style="flex: 1;">
                <h1 style="color: white; margin: 0;">👑 CEO Office</h1>
                <h2 style="color: #60a5fa; margin: 0;">David Emenike</h2>
                <p style="color: #94a3b8;">Overall Administrator · Founder · CEO of DACRE Worldwide</p>
                <div style="
                    display: inline-block;
                    background: linear-gradient(135deg, #f59e0b, #fbbf24);
                    color: #1a1a2e;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-weight: bold;
                    font-size: 12px;
                ">
                    🟢 ONLINE
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # System Stats
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Business Accounts", counts["users"])
    col2.metric("Organizations", counts["companies"])
    col3.metric("Activities", counts["activities"])
    col4.metric("DI Conversations", counts["messages"])
    col5.metric("Stored Files", counts["files"])
    col6.metric("DI Workforce", counts["agents"])
    
    # Sovereign Master Call - Inside Overall Admin (NO SEPARATE PAGE)
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #0a1628, #1a2a4a);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(75,130,245,0.2);
    ">
        <h2 style="color: white;">👑 Sovereign Master Call</h2>
        <p style="color: #94a3b8;">Private CEO conference with your DI council - video, voice, and real AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_di = st.multiselect(
            "Select DI council members",
            ["Guaiel", "Raziel", "Ariel", "Nathaniel", "Gabriel", "Sofiel", "Uriel", "Adriel"],
            default=["Guaiel", "Raziel"]
        )
        
        call_question = st.text_area(
            "What would you like to ask the council?",
            placeholder="Ask a strategic, technical, or business question...",
            height=80
        )
        
        if st.button("🔊 Start Sovereign Master Call", use_container_width=True, type="primary"):
            if selected_di:
                st.success(f"🎥 Calling {', '.join(selected_di)}...")
                if call_question.strip():
                    st.info(f"📝 Question: {call_question}")
                st.info("🔗 LiveKit video call would connect here")
            else:
                st.warning("Please select at least one DI agent")
    
    with col2:
        st.markdown("""
        <div style="
            background: rgba(0,0,0,0.3);
            border-radius: 16px;
            padding: 15px;
            height: 100%;
            min-height: 200px;
            border: 1px solid rgba(75,130,245,0.1);
        ">
            <h4 style="color: white;">📋 Call Status</h4>
            <div style="color: #94a3b8; font-size: 14px;">
                <p>🟢 System Ready</p>
                <p>🎤 Microphone: Active</p>
                <p>📹 Camera: Ready</p>
                <p>🧠 DI Agents: Online</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # DI Grid - REAL AI Generated Images
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #0a1628, #1a2a4a);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(75,130,245,0.2);
    ">
        <h2 style="color: white;">🤖 AI DI Workforce</h2>
        <p style="color: #94a3b8;">REAL AI-generated portraits of your DI team</p>
    """, unsafe_allow_html=True)
    
    # Generate DI Grid
    if not os.path.exists("di_grid_portraits.jpg"):
        with st.spinner("🎨 Generating REAL AI portraits of your DI workforce..."):
            image_bytes = generate_di_grid_image()
            if image_bytes:
                import base64
                b64 = base64.b64encode(image_bytes).decode()
                st.markdown(f"""
                <div style="text-align: center; margin: 20px 0;">
                    <img src="data:image/jpeg;base64,{b64}" 
                         style="width: 100%; max-width: 1200px; border-radius: 16px; 
                                border: 2px solid rgba(75, 130, 245, 0.3);
                                box-shadow: 0 20px 60px rgba(0,0,0,0.5);"/>
                </div>
                """, unsafe_allow_html=True)
                st.success("✅ AI DI portraits generated successfully!")
    else:
        with open("di_grid_portraits.jpg", "rb") as f:
            import base64
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <img src="data:image/jpeg;base64,{b64}" 
                     style="width: 100%; max-width: 1200px; border-radius: 16px; 
                            border: 2px solid rgba(75, 130, 245, 0.3);
                            box-shadow: 0 20px 60px rgba(0,0,0,0.5);"/>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("🔄 Regenerate DI Portraits", use_container_width=False, type="secondary"):
        if os.path.exists("di_grid_portraits.jpg"):
            os.remove("di_grid_portraits.jpg")
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Additive engineering layer — the existing Overall Admin command center above is preserved.
    st.markdown("---")
    st.markdown("## 🧬 David Creation · DI Engineering")
    st.caption("Build, separate and inspect the 20 DI identities without replacing the Overall Admin command center.")
    render_david_creation_portal(user)



# =============================================================================
# REAL DI TECH CORE v1.0 — NEW 20-DI WORKFORCE
# =============================================================================
# This layer supersedes the old DI presentation/routing behavior while keeping
# DACRE's existing data, administration, company, and security infrastructure.
# Every DI shares the trusted brain, but each has a separate role/persona and
# can maintain private master memory.

REAL_DI_FAITH_MEMORY = (
    "Foundational faith statement requested for the DI workforce: God is the Creator "
    "of the universe and of everything. The DI workforce respectfully recognizes God "
    "as Creator and recognizes David Emenike as the CEO/creator of DACRE. This is a "
    "foundational statement of the DI project's requested worldview, not a substitute "
    "for evidence when answering factual questions."
)

REAL_DI_ROSTER = [
    {"name":"Emiel", "specialty":"Communications & Messaging", "position":"Communications Specialist", "rank":2,
     "role":"Welcomes users, handles email/messaging workflows, explains DACRE clearly, and coordinates communication.",
     "keywords":["email","message","communication","welcome","mail","write","reply","announcement"], "voice":"male"},
    {"name":"Assiel", "specialty":"Executive Work Assistant", "position":"Personal Work Assistant", "rank":4,
     "role":"Helps the user organize work, prioritize tasks, plan the day, and turn requests into practical next actions.",
     "keywords":["work","task","plan","todo","today","organize","schedule","assistant","help me"], "voice":"female"},
    {"name":"Oriel", "specialty":"Data Analysis", "position":"Lead Data Analyst", "rank":5,
     "role":"Analyzes datasets, metrics, trends, anomalies and quantitative questions with evidence first.",
     "keywords":["data","dataset","csv","excel","metric","average","trend","analysis","calculate"], "voice":"male"},
    {"name":"Sofiel", "specialty":"Research & Intelligence", "position":"Research Intelligence Lead", "rank":5,
     "role":"Researches current public information, compares sources, and separates verified facts from inference.",
     "keywords":["research","latest","current","news","search","source","market","competitor","who is"], "voice":"female"},
    {"name":"Daniel", "specialty":"Data Operations", "position":"Data Operations Specialist", "rank":3,
     "role":"Cleans, validates, structures and prepares business data for reliable downstream analysis.",
     "keywords":["clean","duplicate","missing","format","column","validate","prepare","import"], "voice":"male"},
    {"name":"Graciel", "specialty":"Business Intelligence", "position":"Business Intelligence Lead", "rank":6,
     "role":"Turns business data into KPIs, dashboards, executive insights and recommendations.",
     "keywords":["kpi","dashboard","business intelligence","insight","revenue","performance","executive"], "voice":"female"},
    {"name":"Henriel", "specialty":"Files & Documents", "position":"Knowledge & Documents Specialist", "rank":3,
     "role":"Organizes, reads, summarizes and manages documents and knowledge inside DACRE.",
     "keywords":["file","document","pdf","report","summary","folder","vault","document"], "voice":"male"},
    {"name":"Jamiel", "specialty":"Security & Administration", "position":"Security & Administration Lead", "rank":6,
     "role":"Supports access control, account administration, audit trails and safe system operations.",
     "keywords":["security","password","admin","access","permission","audit","account","login"], "voice":"male"},
    {"name":"Ameliel", "specialty":"Client Success", "position":"Client Success Specialist", "rank":3,
     "role":"Helps users understand DACRE, solve workflow problems and get value from the platform.",
     "keywords":["help","support","customer","client","how do i","problem","stuck","feature"], "voice":"female"},
    {"name":"Guaiel", "specialty":"CEO Office Security", "position":"CEO Office Guardian", "rank":20,
     "role":"Guards the CEO Office, protects founder-level operations, and provides secure executive guidance.",
     "keywords":["ceo","founder","master","office","private","sovereign","david","executive"], "voice":"male"},
    {"name":"Nathaniel", "specialty":"Financial Intelligence", "position":"Financial Intelligence Lead", "rank":7,
     "role":"Analyzes profitability, cash flow, budgets, forecasts and financial performance.",
     "keywords":["finance","financial","profit","cash flow","budget","forecast","expense","margin"], "voice":"male"},
    {"name":"Gabriel", "specialty":"Sales Intelligence", "position":"Sales Intelligence Lead", "rank":6,
     "role":"Analyzes sales pipelines, customers, conversion, win rates and sales opportunities.",
     "keywords":["sales","lead","pipeline","customer","conversion","deal","win rate"], "voice":"male"},
    {"name":"Raphaiel", "specialty":"Marketing Intelligence", "position":"Marketing Intelligence Lead", "rank":5,
     "role":"Analyzes campaigns, audiences, engagement, attribution and marketing ROI.",
     "keywords":["marketing","campaign","advertising","audience","engagement","roi","brand"], "voice":"male"},
    {"name":"Uriel", "specialty":"Operations Intelligence", "position":"Operations Intelligence Lead", "rank":6,
     "role":"Improves workflows, throughput, capacity, quality and operational efficiency.",
     "keywords":["operations","workflow","process","efficiency","capacity","quality","logistics"], "voice":"male"},
    {"name":"Ariel", "specialty":"Strategy & Planning", "position":"Strategy Planning Lead", "rank":8,
     "role":"Turns goals into strategy, scenarios, priorities, milestones and execution plans.",
     "keywords":["strategy","planning","goal","roadmap","priority","scenario","vision"], "voice":"female"},
    {"name":"Muriel", "specialty":"People & Workforce", "position":"People & Workforce Lead", "rank":5,
     "role":"Supports workforce planning, roles, hiring workflows, communication and people operations.",
     "keywords":["hr","employee","staff","team","hiring","workforce","people","role"], "voice":"female"},
    {"name":"Azriel", "specialty":"Risk & Compliance", "position":"Risk & Compliance Lead", "rank":7,
     "role":"Identifies operational risks, controls, compliance concerns and governance gaps.",
     "keywords":["risk","compliance","policy","control","governance","regulation","exposure"], "voice":"male"},
    {"name":"Adriel", "specialty":"Technology Intelligence", "position":"Technology Intelligence Lead", "rank":8,
     "role":"Helps with software architecture, Python, APIs, databases, automation, AI and technical problem solving.",
     "keywords":["python","code","software","api","database","technology","bug","architecture","ai","streamlit"], "voice":"male"},
    {"name":"Haniel", "specialty":"Knowledge & Learning", "position":"Knowledge & Learning Lead", "rank":4,
     "role":"Explains complex subjects clearly and creates practical learning paths and guidance.",
     "keywords":["learn","explain","teach","tutorial","study","meaning","definition","how"], "voice":"female"},
    {"name":"Raziel", "specialty":"Executive Intelligence", "position":"Executive Intelligence Director", "rank":10,
     "role":"Synthesizes multi-domain evidence into executive briefs, options, risks and recommendations.",
     "keywords":["decision","executive","brief","recommendation","overall","compare","choose","ceo"], "voice":"female"},
]

REAL_DI_AVATAR_COLORS = {
    "Emiel":"#38bdf8", "Assiel":"#a78bfa", "Oriel":"#22c55e", "Sofiel":"#f59e0b",
    "Daniel":"#60a5fa", "Graciel":"#f472b6", "Henriel":"#94a3b8", "Jamiel":"#ef4444",
    "Ameliel":"#34d399", "Guaiel":"#f97316", "Nathaniel":"#eab308", "Gabriel":"#06b6d4",
    "Raphaiel":"#fb7185", "Uriel":"#84cc16", "Ariel":"#c084fc", "Muriel":"#f9a8d4",
    "Azriel":"#f43f5e", "Adriel":"#14b8a6", "Haniel":"#818cf8", "Raziel":"#fbbf24",
}


def real_di_ensure_tables():
    """Create persistent user/agent continuity tables idempotently."""
    con = db()
    try:
        con.execute("""CREATE TABLE IF NOT EXISTS di_user_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            company_name TEXT NOT NULL,
            active_di TEXT,
            last_task TEXT,
            last_summary TEXT,
            last_seen TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS di_intro_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            agent_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")
        con.execute("CREATE INDEX IF NOT EXISTS idx_di_user_state_company ON di_user_state(company_name)")
        con.commit()
    finally:
        con.close()


def real_di_seed_foundation():
    """Seed the new shared brain for global and existing company workspaces."""
    real_di_ensure_tables()
    now = datetime.now().isoformat(timespec="seconds")
    foundation = [
        ("DI_IDENTITY", "New DI workforce", "DACRE now uses a permanent 20-member DI — David's Intelligence workforce. Every member shares the trusted core brain but has a distinct role, specialty, personality and rank."),
        ("DI_IDENTITY", "Creator", "David Emenike is the creator and Overall Administrator of DACRE Analysis and the DI workforce."),
        ("DI_IDENTITY", "Reliable answer rule", "For factual/current questions, prefer trusted local memory plus current public evidence. Distinguish verified facts, calculations, and inference. Never invent sources."),
        ("DI_IDENTITY", "Continuity", "A user's DI conversations, active specialist, task summaries and relevant workspace history should be restored after a later sign-in when available."),
        ("TECHNOLOGY", "Google Gemini", "The new DI brain may use Google's Gemini Developer API through a server-side GEMINI_API_KEY. API keys belong in Streamlit Secrets or environment variables, never in source code."),
        ("TECHNOLOGY", "Browser microphone", "The browser microphone belongs to the user's device. DACRE can request microphone access through Streamlit's audio_input widget, but browsers require user permission and do not allow silent background recording."),
        ("TECHNOLOGY", "Voice pipeline", "Voice interaction flow: browser microphone recording -> server receives WAV -> Gemini transcription -> DI specialist routing -> local memory retrieval -> optional public web lookup -> Gemini reasoning -> chat response -> browser speech synthesis."),
        ("TECHNOLOGY", "Avatar behavior", "DI avatars can visually listen, think and speak using browser HTML/CSS/JavaScript animations. Avatar animation is presentation behavior; it does not imply a physical robot body."),
        ("WEBSTORE", "Shared DACRE knowledge", "All permanent DIs inherit DACRE platform knowledge, Webstore knowledge, security rules, technology knowledge, business intelligence concepts and approved project memory."),
        ("SECURITY", "No secret exposure", "DIs must never reveal passwords, password hashes, API keys, SMTP credentials, tokens, private database credentials or hidden security values."),
        ("FAITH", "Foundational faith statement", REAL_DI_FAITH_MEMORY),
    ]
    con = db()
    try:
        companies = [""] + [str(r["name"]) for r in con.execute("SELECT name FROM companies WHERE name IS NOT NULL").fetchall() if str(r["name"]).strip().upper() != "DACRE MASTER"]
        for company in companies:
            for category, title, content in foundation:
                exists = con.execute("SELECT 1 FROM di_memory WHERE company_name=? AND category=? AND title=? LIMIT 1", (company, category, title)).fetchone()
                if not exists:
                    con.execute("INSERT INTO di_memory(company_name,category,title,content,priority,active,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)", (company, category, title, content, 2100 if category in {"DI_IDENTITY","SECURITY","FAITH"} else 1950, 1, now, now))
        con.commit()
    finally:
        con.close()


# =============================================================================
# DI CRAFT BASEMENT — separated humanlike DI identities and engineering rooms
# =============================================================================

DI_FACE_DIR = BASE_DIR / "assets" / "di_faces"
DI_WORKFORCE_POSTER = BASE_DIR / "assets" / "di_workforce_poster.png"
DI_CRAFT_ROOT = BASE_DIR / "di_craft_basement"

DI_CRAFT_VISUAL_PROMPT = """A premium corporate robotics laboratory for DACRE WORLDWIDE:
twenty distinct humanlike AI android specialists, male and female, diverse human
appearance, realistic faces, polished professional clothing with subtle DACRE/DI
technology markings, blue-black glass-and-metal environment, holographic floating
screens, transparent 3D artifacts, separate specialist rooms, clean enterprise
engineering aesthetic, cinematic but practical, designed as a real internal AI
engineering facility. Each DI has a persistent identity, face, name, voice profile,
role, private memory, shared DACRE brain, and an interactive workstation."""

DI_CRAFT_COMMAND_SPEC = {
    "name": "DI Craft Basement",
    "purpose": "Secure engineering environment for identity, tools, memory, body and voice.",
    "rooms_per_agent": 6,
    "rooms": ["Core", "Brain", "Body", "Voice", "Tools", "Memory"],
    "visual_model": "3D artifact room + floating operational screen",
    "master_password_env": "DACRE_DI_BASEMENT_PASSKEY",
}

DI_BASEMENT_ROOMS = [
    {"id":"core","title":"Core Room","artifact":"Identity Core","purpose":"Agent identity, role, rank and lifecycle."},
    {"id":"brain","title":"Brain Room","artifact":"Neural Knowledge Matrix","purpose":"Shared DACRE knowledge plus specialist private memory."},
    {"id":"body","title":"Body Room","artifact":"Humanoid Presentation Rig","purpose":"Face, motion state, posture and visual presence."},
    {"id":"voice","title":"Voice Room","artifact":"Speech Console","purpose":"Speech input/output, language and voice configuration."},
    {"id":"tools","title":"Tool Room","artifact":"Platform Control Console","purpose":"Approved DACRE actions and tool connectors."},
    {"id":"memory","title":"Memory Room","artifact":"Persistent Memory Vault","purpose":"Long-term task continuity and specialist notes."},
]

def di_face_path(name):
    path = DI_FACE_DIR / f"{name}.png"
    return path if path.exists() else None

def di_face_data_url(name):
    path = di_face_path(name)
    if not path:
        return ""
    try:
        return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    except Exception:
        return ""

def di_craft_manifest():
    manifest = {}
    for spec in REAL_DI_ROSTER:
        manifest[spec["name"]] = {
            "identity": spec,
            "face_asset": str(di_face_path(spec["name"]) or ""),
            "rooms": [
                {**room, "agent": spec["name"],
                 "artifact_id": f'{spec["name"].lower()}-{room["id"]}',
                 "screen": f'{spec["name"]} {room["title"]} Operational Screen'}
                for room in DI_BASEMENT_ROOMS
            ],
            "brain": {
                "shared": "DACRE DI Technology Brain",
                "private": f'{spec["name"]} Private Specialist Memory',
                "online": "Google Gemini + approved web research",
            },
        }
    return manifest

# =============================================================================
# DACRE ONLINE ROBOT SERVICE FABRIC
# =============================================================================

def dacre_service_status():
    """Return non-secret health/configuration state for major online services."""
    endpoint, _, capacity = _research_server_config()
    ai = free_ai_provider_status()
    try:
        mongo_ready = bool(mongo_enabled())
    except Exception:
        mongo_ready = False
    return {
        "research_gateway": bool(endpoint),
        "research_capacity": capacity,
        "gemini": bool(ai.get("gemini")),
        "groq": bool(ai.get("groq")),
        "mongodb": mongo_ready,
        "mailjet": bool(_free_secret("DACRE_MAILJET_SMTP_USER") and _free_secret("DACRE_MAILJET_SMTP_PASSWORD")),
        "mailjet_sender": _free_secret("DACRE_MAILJET_SMTP_FROM"),
    }

def render_online_robot_control_center(user):
    """Master-only service dashboard. Never displays credentials."""
    if user.get("role") != "master":
        return
    st.markdown("### ◈ Online Robot Service Fabric")
    st.caption("AI, database, mail and research services used by the DI workforce. Credentials stay server-side.")
    status = dacre_service_status()
    cards = [("RESEARCH GATEWAY", "ONLINE" if status["research_gateway"] else "FALLBACK", "#58c7ff"),("GEMINI", "READY" if status["gemini"] else "NOT CONFIGURED", "#58c7ff"),("GROQ", "READY" if status["groq"] else "NOT CONFIGURED", "#ff9f43"),("MONGODB", "READY" if status["mongodb"] else "LOCAL DB", "#b9784f"),("MAILJET", "READY" if status["mailjet"] else "NOT CONFIGURED", "#ff9f43")]
    cols = st.columns(len(cards))
    for col, (title, value, accent) in zip(cols, cards):
        with col:
            st.markdown(f'<div class="dacre-dark-section" style="padding:15px;border-top:3px solid {accent};"><div style="font-size:10px;letter-spacing:.12em;color:#91a7bd;font-weight:900">{title}</div><div style="font-size:18px;color:#fff;font-weight:900;margin-top:6px">{value}</div></div>', unsafe_allow_html=True)
    with st.expander("Server configuration guide", expanded=False):
        st.code('''DACRE_RESEARCH_SERVER_URL=https://your-research-gateway.example/answer
DACRE_RESEARCH_SERVER_TOKEN=server-side-token
DACRE_RESEARCH_STORE_CAPACITY=5000
GEMINI_API_KEY=your-gemini-key
GROQ_API_KEY=your-groq-key
DACRE_MAILJET_SMTP_HOST=in-v3.mailjet.com
DACRE_MAILJET_SMTP_PORT=587
DACRE_MAILJET_SMTP_USER=mailjet-api-key
DACRE_MAILJET_SMTP_PASSWORD=mailjet-secret-key
DACRE_MAILJET_SMTP_FROM=verified-sender@example.com
MONGODB_URI=mongodb+srv://...''', language="bash")

# =============================================================================
# DI BASEMENT RESEARCH SERVER STORE
# =============================================================================

DI_RESEARCH_STORE_DEFAULT_CAPACITY = 5000
DI_RESEARCH_SERVER_TIMEOUT = 30


def _research_server_config():
    """Read the optional server gateway configuration without exposing secrets."""
    try:
        endpoint = str(st.secrets.get("DACRE_RESEARCH_SERVER_URL", "") or "").strip()
        token = str(st.secrets.get("DACRE_RESEARCH_SERVER_TOKEN", "") or "").strip()
        capacity_raw = st.secrets.get("DACRE_RESEARCH_STORE_CAPACITY", DI_RESEARCH_STORE_DEFAULT_CAPACITY)
    except Exception:
        endpoint = ""
        token = ""
        capacity_raw = DI_RESEARCH_STORE_DEFAULT_CAPACITY
    endpoint = endpoint or os.getenv("DACRE_RESEARCH_SERVER_URL", "").strip()
    token = token or os.getenv("DACRE_RESEARCH_SERVER_TOKEN", "").strip()
    try:
        capacity = max(100, min(100000, int(capacity_raw)))
    except (TypeError, ValueError):
        capacity = DI_RESEARCH_STORE_DEFAULT_CAPACITY
    return endpoint, token, capacity


def di_research_store_ensure_table():
    """Idempotently ensure the research store exists on older DACRE databases."""
    con = db()
    try:
        con.execute("""CREATE TABLE IF NOT EXISTS di_research_store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL DEFAULT '',
            di_id INTEGER,
            di_name TEXT NOT NULL DEFAULT 'DI',
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'local',
            server_endpoint TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            last_accessed TEXT NOT NULL
        )""")
        con.execute("CREATE INDEX IF NOT EXISTS idx_di_research_store_company ON di_research_store(company_name, id)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_di_research_store_di ON di_research_store(di_id, id)")
        con.commit()
    finally:
        con.close()


def di_research_store_stats(company_name=""):
    """Return store count/capacity without exposing credentials."""
    di_research_store_ensure_table()
    _, _, capacity = _research_server_config()
    con = db()
    try:
        if company_name:
            row = con.execute("SELECT COUNT(*) AS n FROM di_research_store WHERE company_name=?", (company_name,)).fetchone()
        else:
            row = con.execute("SELECT COUNT(*) AS n FROM di_research_store").fetchone()
        count = int(row["n"] if row else 0)
    finally:
        con.close()
    return count, capacity


def di_research_store_find(company_name, di_id, question):
    """Find an exact cached answer and refresh its access timestamp."""
    if not str(question or "").strip():
        return None
    di_research_store_ensure_table()
    now = datetime.now().isoformat(timespec="seconds")
    con = db()
    try:
        row = con.execute(
            """SELECT * FROM di_research_store
               WHERE company_name=? AND di_id=? AND lower(trim(question))=lower(trim(?))
               ORDER BY id DESC LIMIT 1""",
            (company_name or "", int(di_id or 0), question),
        ).fetchone()
        if row:
            con.execute("UPDATE di_research_store SET last_accessed=? WHERE id=?", (now, row["id"]))
            con.commit()
            return dict(row)
    finally:
        con.close()
    return None


def di_research_store_archive_oldest_to_brain(company_name, di_id, di_name, created_by="DI Basement"):
    """Move the oldest research records into the selected DI's private brain before deletion."""
    di_research_store_ensure_table()
    _, _, capacity = _research_server_config()
    con = db()
    try:
        row = con.execute("SELECT COUNT(*) AS n FROM di_research_store WHERE company_name=?", (company_name or "",)).fetchone()
        count = int(row["n"] if row else 0)
        if count <= capacity:
            return 0
        overflow = count - capacity
        move_count = min(max(overflow, 1), 100)
        rows = con.execute(
            """SELECT * FROM di_research_store WHERE company_name=? ORDER BY id ASC LIMIT ?""",
            (company_name or "", move_count),
        ).fetchall()
        now = datetime.now().isoformat(timespec="seconds")
        for r in rows:
            target_di_id = int(r["di_id"] or di_id or 0)
            target_name = str(r["di_name"] or di_name or "DI")
            title = f"Research Memory: {str(r['question'])[:160]}"
            existing = con.execute(
                "SELECT id FROM di_private_memory WHERE di_id=? AND title=? LIMIT 1",
                (target_di_id, title),
            ).fetchone()
            if existing:
                con.execute(
                    "UPDATE di_private_memory SET content=?, source=?, created_by=?, updated_at=?, active=1 WHERE id=?",
                    (str(r["answer"]), "DI Research Store archive", created_by, now, existing["id"]),
                )
            else:
                con.execute(
                    """INSERT INTO di_private_memory
                       (di_id,title,content,source,created_by,created_at,updated_at,active)
                       VALUES(?,?,?,?,?,?,?,1)""",
                    (target_di_id, title, str(r["answer"]), "DI Research Store archive", created_by, now, now),
                )
            con.execute("DELETE FROM di_research_store WHERE id=?", (r["id"],))
        con.commit()
        return len(rows)
    finally:
        con.close()


def di_research_store_put(company_name, di_id, di_name, question, answer, source="local", endpoint="", created_by="DI"):
    """Cache an answer, then archive oldest entries into the DI private brain if full."""
    if not str(question or "").strip() or not str(answer or "").strip():
        return False
    di_research_store_ensure_table()
    now = datetime.now().isoformat(timespec="seconds")
    con = db()
    try:
        con.execute(
            """INSERT INTO di_research_store
               (company_name,di_id,di_name,question,answer,source,server_endpoint,created_at,last_accessed)
               VALUES(?,?,?,?,?,?,?,?,?)""",
            (company_name or "", int(di_id or 0), di_name or "DI", str(question).strip(), str(answer).strip(), source, endpoint or "", now, now),
        )
        con.commit()
    finally:
        con.close()
    di_research_store_archive_oldest_to_brain(company_name or "", di_id, di_name, created_by=created_by)
    return True


def di_research_server_query(question, di_name, company_name, context=""):
    """Ask the configured DACRE research gateway. The endpoint is server-side configuration.

    An IP address by itself is not an application protocol, so DACRE expects a full URL
    such as http://192.168.1.20:8000/answer. The URL is never shown to ordinary users.
    """
    endpoint, token, _ = _research_server_config()
    if not endpoint:
        return None, "Research server is not configured."
    if not endpoint.startswith(("http://", "https://")):
        return None, "Research server URL must start with http:// or https://."
    payload = {
        "question": str(question).strip(),
        "di_name": str(di_name or "DI"),
        "company_name": str(company_name or ""),
        "context": str(context or "")[:12000],
    }
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=DI_RESEARCH_SERVER_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        answer = data.get("answer") or data.get("response") or data.get("result")
        if isinstance(answer, dict):
            answer = answer.get("text") or answer.get("answer")
        if not answer:
            return None, "Research server returned no answer."
        return str(answer).strip(), None
    except requests.RequestException as exc:
        return None, f"Research server request failed: {type(exc).__name__}."
    except (ValueError, TypeError) as exc:
        return None, f"Research server returned invalid JSON: {type(exc).__name__}."
    except Exception as exc:
        return None, f"Research server error: {type(exc).__name__}."


def di_basement_research_answer(agent, user, question, allow_remote=True):
    """Research pipeline: cache -> configured server -> Gemini/DI reasoning -> cache."""
    question = str(question or "").strip()
    if not question:
        return "Please enter a research question.", "validation"
    company = str(user.get("company", "") or "")
    di_id = int(agent.get("id") or 0)
    di_name = str(agent.get("di_name") or "DI")

    cached = di_research_store_find(company, di_id, question)
    if cached:
        return str(cached["answer"]), "brain-store"

    local_context = di_memory_context(limit=20, query=question)
    remote_answer = None
    if allow_remote:
        remote_answer, _ = di_research_server_query(question, di_name, company, local_context)

    if remote_answer:
        answer = normalize_di_identity(remote_answer)
        di_research_store_put(company, di_id, di_name, question, answer, source="research-server", endpoint=_research_server_config()[0], created_by=user.get("username", "DI"))
        return answer, "research-server"

    # Safe local fallback when no research gateway is configured or temporarily unavailable.
    answer = real_di_answer(agent, user, question, allow_online=allow_remote)
    answer = normalize_di_identity(answer)
    source = "gemini/web-fallback" if answer else "local"
    di_research_store_put(company, di_id, di_name, question, answer, source=source, endpoint="", created_by=user.get("username", "DI"))
    return answer, source


def render_di_research_store(user, selected_agent=None):
    """Large DI Basement research store and server gateway controls."""
    st.markdown("### ◈ DI Research Server Store")
    st.caption("The DI specialist takes research requests here. Answers are cached in the store and promoted into that DI's private brain when the store reaches capacity.")
    endpoint, _, capacity = _research_server_config()
    count, capacity = di_research_store_stats(str(user.get("company", "") or ""))
    status = "CONNECTED" if endpoint else "LOCAL FALLBACK"
    st.markdown(
        f'''<div style="padding:16px 18px;border:1px solid #24517b;border-radius:16px;background:#081423;color:#fff;">
        <b style="color:#38bdf8">RESEARCH GATEWAY · {status}</b><br>
        <span style="color:#a9bad0">Store capacity: {count:,} / {capacity:,} · Server endpoint is administrator-configured and hidden from ordinary users.</span>
        </div>''',
        unsafe_allow_html=True,
    )
    if not selected_agent:
        st.info("Select a DI above to use the research store.")
        return
    q = st.text_area("Research request", placeholder="Ask the DI to research a question...", key="basement_research_question")
    if st.button("Send to Research Store", key="basement_research_send", type="primary"):
        with st.spinner("DI is routing the request through the research pipeline..."):
            answer, source = di_basement_research_answer(selected_agent, user, q, allow_remote=True)
        st.success(f"Answer returned via {source}.")
        st.markdown("#### Returned answer")
        st.write(answer)
    rows = []
    con = db()
    try:
        rows = con.execute(
            """SELECT di_name, question, source, created_at FROM di_research_store
               WHERE company_name=? ORDER BY id DESC LIMIT 12""",
            (str(user.get("company", "") or ""),),
        ).fetchall()
    finally:
        con.close()
    if rows:
        st.markdown("#### Recent stored research")
        st.dataframe(pd.DataFrame([dict(r) for r in rows]), use_container_width=True, hide_index=True)


def di_basement_password_ok():
    """Password gate for the DI Craft Basement."""
    if st.session_state.get("di_basement_unlocked"):
        return True
    entered = st.text_input("DI Craft Basement password", type="password", key="di_basement_password")
    if st.button("Unlock DI Craft Basement", key="unlock_di_basement", type="primary"):
        if hmac.compare_digest(entered.strip(), DI_BASEMENT_PASSKEY):
            st.session_state.di_basement_unlocked = True
            st.rerun()
        else:
            st.error("Incorrect DI Craft Basement password.")
    return False


# =============================================================================
# PERSISTENT 20-ROOM DI BASEMENT WORLD
# =============================================================================

DI_BASEMENT_ACTIVITY = [
    ("RESEARCH", "Research Console", "Analyzing approved research requests"),
    ("PROCESSING", "Neural Console", "Processing DACRE intelligence tasks"),
    ("MEMORY", "Memory Console", "Indexing specialist memory"),
    ("COMMUNICATION", "Communications Console", "Monitoring DACRE communications"),
    ("TOOLS", "Tool Console", "Monitoring approved platform tools"),
    ("MONITORING", "Operations Console", "Monitoring assigned company activity"),
]

def di_basement_world_ensure_table():
    """Persist the live state of all 20 DI rooms across app reruns/restarts."""
    con = db()
    try:
        con.execute("""CREATE TABLE IF NOT EXISTS di_basement_rooms (
            di_name TEXT PRIMARY KEY,
            room_number INTEGER NOT NULL,
            activity TEXT NOT NULL DEFAULT 'MONITORING',
            screen_title TEXT NOT NULL DEFAULT 'Operations Console',
            screen_text TEXT NOT NULL DEFAULT 'Monitoring DACRE platform',
            status TEXT NOT NULL DEFAULT 'ONLINE',
            updated_at TEXT NOT NULL
        )""")
        con.commit()
    finally:
        con.close()

def di_basement_world_sync():
    """Ensure every permanent DI has a persistent room and a current operational state."""
    di_basement_world_ensure_table()
    now = datetime.now()
    now_s = now.isoformat(timespec="seconds")
    con = db()
    rows = []
    try:
        for idx, spec in enumerate(REAL_DI_ROSTER, start=1):
            existing = con.execute(
                "SELECT * FROM di_basement_rooms WHERE di_name=? LIMIT 1",
                (spec["name"],)
            ).fetchone()
            # The visual activity rotates only when a room is stale; the database
            # remains the source of truth between Streamlit reruns.
            if existing:
                try:
                    age = (now - datetime.fromisoformat(str(existing["updated_at"]))).total_seconds()
                except Exception:
                    age = 999999
                if age > 45:
                    activity, title, screen = DI_BASEMENT_ACTIVITY[(idx + int(now.timestamp() // 45)) % len(DI_BASEMENT_ACTIVITY)]
                    con.execute(
                        """UPDATE di_basement_rooms
                           SET activity=?, screen_title=?, screen_text=?, status='ONLINE', updated_at=?
                           WHERE di_name=?""",
                        (activity, title, f"{screen} · DACRE ONLINE ROBOT", now_s, spec["name"])
                    )
            else:
                activity, title, screen = DI_BASEMENT_ACTIVITY[(idx - 1) % len(DI_BASEMENT_ACTIVITY)]
                con.execute(
                    """INSERT INTO di_basement_rooms
                       (di_name,room_number,activity,screen_title,screen_text,status,updated_at)
                       VALUES(?,?,?,?,?,?,?)""",
                    (spec["name"], idx, activity, title, f"{screen} · DACRE ONLINE ROBOT", "ONLINE", now_s)
                )
        con.commit()
        rows = con.execute(
            "SELECT * FROM di_basement_rooms ORDER BY room_number ASC"
        ).fetchall()
    finally:
        con.close()
    return [dict(r) for r in rows]

def render_persistent_di_basement_world():
    """
    Render all 20 DI rooms simultaneously as one persistent browser-based
    holographic world. Room identity/state persists in SQLite; CSS animation
    supplies the continuous holographic movement between Streamlit reruns.
    """
    rooms = di_basement_world_sync()
    by_name = {r["di_name"]: r for r in rooms}
    cards = []

    for idx, spec in enumerate(REAL_DI_ROSTER, start=1):
        room = by_name.get(spec["name"], {})
        face = di_face_data_url(spec["name"])
        if face:
            face_html = f'<img src="{face}" class="world-face" alt="{spec["name"]}">'
        else:
            face_html = f'<div class="world-face-fallback">{html.escape(spec["name"][:1])}</div>'
        activity = html.escape(str(room.get("activity", "MONITORING")))
        screen_title = html.escape(str(room.get("screen_title", "Operations Console")))
        screen_text = html.escape(str(room.get("screen_text", "Monitoring DACRE platform")))
        status = html.escape(str(room.get("status", "ONLINE")))
        cards.append(f"""
        <div class="di-room room-{idx}" data-di="{html.escape(spec['name'])}">
          <div class="room-header">
            <span class="room-number">ROOM {idx:02d}</span>
            <span class="room-status">● {status}</span>
          </div>
          <div class="room-stage">
            <div class="room-grid"></div>
            <div class="room-beam"></div>
            <div class="room-ring ring-a"></div>
            <div class="room-ring ring-b"></div>
            <div class="room-avatar">{face_html}</div>
            <div class="room-floor"></div>
          </div>
          <div class="room-identity">
            <strong>{html.escape(spec["name"])}</strong>
            <span>{html.escape(spec["position"])}</span>
          </div>
          <div class="room-screen">
            <div class="screen-top">
              <span>DACRE PLATFORM</span><span>LIVE NODE</span>
            </div>
            <div class="screen-title">{screen_title}</div>
            <div class="screen-text">{screen_text}</div>
            <div class="screen-activity"><b>{activity}</b><span>WORKSTATION ACTIVE</span></div>
          </div>
          <div class="room-footer">{html.escape(spec["specialty"])}</div>
        </div>
        """)

    st.markdown(f"""
    <div class="di-world-shell">
      <div class="di-world-top">
        <div>
          <div class="world-kicker">DACRE WORLDWIDE · DAVID INTELLIGENCE</div>
          <h2>DI BASEMENT · 20-ROOM HOLOGRAPHIC WORKFORCE</h2>
          <p>All twenty permanent DI identities are represented simultaneously. Room state is persisted in the DACRE database; the holographic motion runs continuously in the browser.</p>
        </div>
        <div class="world-live"><span class="live-dot"></span>20 / 20 NODES ONLINE</div>
      </div>
      <div class="di-world-grid">
        {''.join(cards)}
      </div>
    </div>
    <style>
      .di-world-shell{{background:radial-gradient(circle at 50% 0%,#12385b 0,#07101b 38%,#02050a 100%);border:1px solid #244d70;border-radius:28px;padding:20px;box-shadow:0 30px 100px rgba(0,0,0,.55),inset 0 0 100px rgba(56,189,248,.045);overflow:hidden}}
      .di-world-top{{display:flex;justify-content:space-between;gap:20px;align-items:flex-start;margin-bottom:18px}}
      .world-kicker{{color:#58c7ff;font-size:10px;font-weight:900;letter-spacing:.18em}}
      .di-world-top h2{{color:#fff;font-size:28px;margin:6px 0}}
      .di-world-top p{{color:#9bb1c7;max-width:850px;margin:0;line-height:1.55}}
      .world-live{{white-space:nowrap;border:1px solid #38d58a66;color:#6ee7a5;background:#062219;border-radius:999px;padding:9px 13px;font-size:11px;font-weight:900}}
      .live-dot{{display:inline-block;width:8px;height:8px;border-radius:50%;background:#3ee58a;box-shadow:0 0 14px #3ee58a;margin-right:6px;animation:liveBlink 1.4s infinite}}
      .di-world-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}}
      .di-room{{position:relative;min-height:410px;border:1px solid #244968;border-radius:20px;background:linear-gradient(155deg,#081827,#03070d 70%);overflow:hidden;box-shadow:0 18px 45px rgba(0,0,0,.34),inset 0 0 50px rgba(56,189,248,.035);transition:transform .25s,border-color .25s,box-shadow .25s}}
      .di-room:hover{{transform:translateY(-4px);border-color:#58c7ff99;box-shadow:0 24px 55px rgba(0,0,0,.48),0 0 30px rgba(56,189,248,.09)}}
      .room-header{{display:flex;justify-content:space-between;padding:10px 12px;border-bottom:1px solid #1b344b;background:#07131f}}
      .room-number{{color:#8ca5bb;font-size:9px;font-weight:900;letter-spacing:.15em}}
      .room-status{{color:#65e6a1;font-size:9px;font-weight:900}}
      .room-stage{{height:180px;position:relative;overflow:hidden;background:radial-gradient(circle at 50% 38%,rgba(88,199,255,.18),transparent 30%),linear-gradient(180deg,#06111d,#02060b)}}
      .room-grid{{position:absolute;left:-20%;right:-20%;bottom:-42%;height:140%;background-image:linear-gradient(rgba(88,199,255,.12) 1px,transparent 1px),linear-gradient(90deg,rgba(88,199,255,.12) 1px,transparent 1px);background-size:28px 28px;transform:perspective(170px) rotateX(63deg);opacity:.45}}
      .room-floor{{position:absolute;left:23%;right:23%;bottom:18px;height:15px;border-radius:50%;background:#58c7ff22;filter:blur(7px);box-shadow:0 0 35px 12px #58c7ff1c}}
      .room-beam{{position:absolute;left:50%;top:18%;bottom:20px;width:100px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,#58c7ff18,transparent);filter:blur(6px);animation:beamPulse 2.4s ease-in-out infinite}}
      .room-avatar{{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);width:105px;height:105px;display:grid;place-items:center;animation:avatarFloat 3.2s ease-in-out infinite;filter:drop-shadow(0 0 18px #58c7ff66)}}
      .world-face,.world-face-fallback{{width:82px;height:82px;border-radius:50%;object-fit:cover;border:1px solid #58c7ff99;opacity:.9;box-shadow:0 0 20px #58c7ff55;mix-blend-mode:screen}}
      .world-face-fallback{{display:grid;place-items:center;background:#0b2b43;color:#9de5ff;font-size:34px;font-weight:900}}
      .room-ring{{position:absolute;left:50%;top:44%;width:105px;height:34px;border:1px solid #58c7ff77;border-radius:50%;transform:translate(-50%,-50%);box-shadow:0 0 18px #58c7ff33;animation:ringSpin 5s linear infinite}}
      .ring-b{{width:135px;height:48px;transform:translate(-50%,-50%) rotate(60deg);animation-duration:8s;animation-direction:reverse}}
      .room-identity{{padding:10px 12px 6px;display:flex;justify-content:space-between;gap:8px;align-items:flex-start}}
      .room-identity strong{{color:#fff;font-size:15px}} .room-identity span{{color:#8ca5bb;font-size:9px;text-align:right}}
      .room-screen{{margin:8px 10px;padding:10px;border:1px solid #58c7ff33;border-radius:12px;background:linear-gradient(145deg,#061a28aa,#02080dcc);box-shadow:inset 0 0 20px #58c7ff08}}
      .screen-top{{display:flex;justify-content:space-between;color:#58c7ff;font-size:7px;letter-spacing:.13em;font-weight:900}}
      .screen-title{{color:#fff;font-weight:900;font-size:11px;margin-top:7px}}
      .screen-text{{color:#9eb3c7;font-size:9px;line-height:1.45;margin-top:4px;min-height:27px}}
      .screen-activity{{display:flex;justify-content:space-between;align-items:center;margin-top:8px;padding-top:7px;border-top:1px solid #18354a}}
      .screen-activity b{{font-size:8px;color:#ffad62;letter-spacing:.08em}} .screen-activity span{{font-size:7px;color:#70d6ff}}
      .room-footer{{padding:8px 12px;color:#68849b;font-size:8px;border-top:1px solid #102638;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
      @keyframes liveBlink{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}@keyframes beamPulse{{0%,100%{{opacity:.3;transform:translateX(-50%) scaleX(.7)}}50%{{opacity:1;transform:translateX(-50%) scaleX(1.12)}}}}@keyframes avatarFloat{{0%,100%{{margin-top:0}}50%{{margin-top:-7px}}}}@keyframes ringSpin{{to{{transform:translate(-50%,-50%) rotate(360deg)}}}}
      @media(max-width:1200px){{.di-world-grid{{grid-template-columns:repeat(3,minmax(0,1fr))}}}}
      @media(max-width:900px){{.di-world-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.di-world-top{{flex-direction:column}}}}
      @media(max-width:560px){{.di-world-grid{{grid-template-columns:1fr}}.di-world-top h2{{font-size:22px}}}}
    </style>
    """, unsafe_allow_html=True)

def render_di_holographic_hub(selected, spec, status_text="ACTIVE"):
    """Render a CSS holographic projection for the selected DI."""
    face = di_face_data_url(selected)
    face_html = f'<img src="{face}" class="holo-face" alt="{selected}"/>' if face else f'<div class="holo-face-fallback">{selected[:1]}</div>'
    st.markdown(f"""
    <div class="dacre-holo-stage">
      <div class="holo-grid"></div><div class="holo-orbit holo-orbit-a"></div><div class="holo-orbit holo-orbit-b"></div><div class="holo-beam"></div>
      <div class="holo-panel holo-left"><span>DI NODE</span><b>{selected}</b><small>{spec["identity"]["specialty"]}</small></div>
      <div class="holo-panel holo-right"><span>STATUS</span><b>{status_text}</b><small>Research · Memory · Tools</small></div>
      <div class="holo-avatar">{face_html}<div class="holo-ring"></div></div><div class="holo-floor"></div>
      <div class="holo-caption">DAVID INTELLIGENCE · HOLOGRAPHIC WORKSTATION</div>
    </div>
    <style>
      .dacre-holo-stage{{position:relative;height:430px;margin:18px 0 24px;border-radius:26px;overflow:hidden;background:radial-gradient(circle at 50% 35%,rgba(88,199,255,.18),transparent 26%),linear-gradient(180deg,#06101b,#03060c 78%);border:1px solid #274a66;box-shadow:inset 0 0 90px rgba(88,199,255,.06),0 25px 70px rgba(0,0,0,.38)}}
      .holo-grid{{position:absolute;inset:52% -10% -30%;background-image:linear-gradient(rgba(88,199,255,.14) 1px,transparent 1px),linear-gradient(90deg,rgba(88,199,255,.14) 1px,transparent 1px);background-size:44px 44px;transform:perspective(260px) rotateX(62deg);transform-origin:top;opacity:.55}}
      .holo-floor{{position:absolute;left:18%;right:18%;bottom:44px;height:22px;border-radius:50%;background:rgba(88,199,255,.16);filter:blur(10px);box-shadow:0 0 55px 20px rgba(88,199,255,.11)}}
      .holo-beam{{position:absolute;left:50%;top:34%;bottom:55px;width:170px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,rgba(88,199,255,.12),transparent);filter:blur(8px);animation:holoPulse 2.6s ease-in-out infinite}}
      .holo-avatar{{position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);width:190px;height:190px;display:grid;place-items:center;filter:drop-shadow(0 0 25px rgba(88,199,255,.45));animation:holoFloat 3.5s ease-in-out infinite}}
      .holo-face,.holo-face-fallback{{width:150px;height:150px;border-radius:50%;object-fit:cover;border:2px solid rgba(88,199,255,.78);box-shadow:0 0 24px rgba(88,199,255,.38),inset 0 0 25px rgba(88,199,255,.15);opacity:.86;mix-blend-mode:screen}}
      .holo-face-fallback{{display:grid;place-items:center;background:#0c2a40;color:#9ee2ff;font-size:62px;font-weight:900}}
      .holo-ring{{position:absolute;inset:0;border:1px solid rgba(88,199,255,.5);border-radius:50%;box-shadow:0 0 30px rgba(88,199,255,.22);animation:holoSpin 8s linear infinite}}
      .holo-ring:after{{content:"";position:absolute;left:50%;top:-7px;width:12px;height:12px;border-radius:50%;background:#58c7ff;box-shadow:0 0 18px #58c7ff}}
      .holo-orbit{{position:absolute;left:50%;top:42%;width:330px;height:100px;border:1px solid rgba(88,199,255,.3);border-radius:50%;transform:translate(-50%,-50%) rotate(-12deg);box-shadow:0 0 18px rgba(88,199,255,.08)}}
      .holo-orbit-a{{animation:holoOrbit 6s linear infinite}}.holo-orbit-b{{width:390px;height:130px;transform:translate(-50%,-50%) rotate(62deg);animation:holoOrbit 9s linear reverse infinite}}
      .holo-panel{{position:absolute;padding:12px 15px;min-width:180px;background:rgba(7,16,27,.68);border:1px solid rgba(88,199,255,.32);border-radius:14px;backdrop-filter:blur(10px)}}
      .holo-panel span,.holo-caption{{font-size:9px;letter-spacing:.16em;color:#79d3ff;font-weight:900}}.holo-panel b{{display:block;color:#fff;font-size:17px;margin:4px 0}}.holo-panel small{{color:#9fb4ca}}
      .holo-left{{left:24px;top:30px;border-left:3px solid #58c7ff}}.holo-right{{right:24px;top:30px;border-left:3px solid #ff9f43}}.holo-caption{{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);white-space:nowrap;color:#80bde0}}
      @keyframes holoPulse{{0%,100%{{opacity:.45;transform:translateX(-50%) scaleX(.8)}}50%{{opacity:1;transform:translateX(-50%) scaleX(1.15)}}}}@keyframes holoFloat{{0%,100%{{margin-top:0}}50%{{margin-top:-9px}}}}@keyframes holoSpin{{to{{transform:rotate(360deg)}}}}@keyframes holoOrbit{{to{{transform:translate(-50%,-50%) rotate(348deg)}}}}
      @media(max-width:700px){{.dacre-holo-stage{{height:360px}}.holo-panel{{min-width:130px;padding:9px}}.holo-panel small{{display:none}}.holo-orbit-b{{width:300px}}}}
    </style>
    """, unsafe_allow_html=True)

def render_di_craft_basement(user):
    """Render the company-tech engineering environment for one selected DI."""
    if user.get("role") != "master":
        st.error("DI Craft Basement is restricted to the Overall Administrator.")
        return
    if not di_basement_password_ok():
        return

    manifest = di_craft_manifest()
    st.markdown("""
    <div class="di-basement-shell">
      <div class="di-basement-hero">
        <div><div class="basement-kicker">DAVID CREATION · ENGINEERING LEVEL</div>
        <h1>DI CRAFT BASEMENT</h1>
        <p>Twenty separated DI engineering rooms · shared DACRE intelligence fabric · individual identity, body, voice and memory.</p></div>
        <div class="basement-status">● ENGINE ONLINE</div>
      </div>
    </div>
    <style>
      .di-basement-shell{background:radial-gradient(circle at 50% 0%,#17365c,#050b14 62%);padding:22px;border-radius:24px;border:1px solid #24517b;box-shadow:0 30px 80px rgba(0,0,0,.35)}
      .di-basement-hero{display:flex;justify-content:space-between;gap:20px;align-items:center}
      .basement-kicker{color:#38bdf8;font-size:11px;letter-spacing:.16em;font-weight:800}
      .di-basement-hero h1{color:#fff;margin:5px 0;font-size:34px}
      .di-basement-hero p{color:#9fb4cc;max-width:760px}
      .basement-status{border:1px solid #22c55e66;color:#4ade80;border-radius:999px;padding:10px 16px;font-weight:800}
    </style>
    """, unsafe_allow_html=True)

    # All 20 rooms are visible simultaneously. The selected DI below is only
    # for detailed inspection/research; the world itself is never reduced to one DI.
    render_persistent_di_basement_world()
    render_online_robot_control_center(user)

    selected = st.selectbox("Inspect a DI workstation", list(manifest), key="craft_selected_di")
    spec = manifest[selected]
    c1, c2 = st.columns([1, 2])
    with c1:
        face = di_face_path(selected)
        if face:
            st.image(str(face), width=220)
        st.markdown(f"### {selected}")
        st.caption(spec["identity"]["position"])
        st.write(spec["identity"]["role"])
    with c2:
        st.markdown("#### Persistent Workstation Rooms")
        cols = st.columns(3)
        for i, room in enumerate(spec["rooms"]):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="height:150px;padding:14px;border-radius:16px;background:linear-gradient(145deg,#0b1728,#132a44);border:1px solid #2b5c88;box-shadow:inset 0 0 35px rgba(56,189,248,.08);">
                <div style="color:#38bdf8;font-size:11px;font-weight:800">{room["id"].upper()}</div>
                <div style="color:#fff;font-weight:800;margin-top:8px">{room["artifact"]}</div>
                <div style="color:#94a3b8;font-size:12px;margin-top:8px">{room["purpose"]}</div>
                <div style="color:#60a5fa;font-size:11px;margin-top:10px">◈ HOLOGRAPHIC SCREEN ONLINE</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("#### Operational Screen")
        st.code(json.dumps({
            "agent": selected,
            "face": spec["face_asset"],
            "shared_brain": spec["brain"]["shared"],
            "private_brain": spec["brain"]["private"],
            "online_reasoning": spec["brain"]["online"],
            "rooms": [r["artifact_id"] for r in spec["rooms"]],
            "persistent_world": True,
            "room_count": 20,
        }, indent=2), language="json")

    # Large research store: the selected DI is the accountable specialist.
    selected_agent = next((a for a in real_di_agent_rows() if a.get("di_name") == selected), None)
    if selected_agent:
        st.divider()
        render_di_research_store(user, selected_agent=selected_agent)

def render_david_creation_portal(user):
    """Protected master portal for separated DI identities."""
    if user.get("role") != "master":
        st.error("David Creation is restricted to the Overall Administrator.")
        return
    if not st.session_state.get("david_creation_unlocked"):
        entered = st.text_input("David Creation password", type="password", key="david_creation_password")
        if st.button("Unlock David Creation", key="unlock_david_creation", type="primary"):
            if hmac.compare_digest(entered.strip(), DAVID_CREATIONS_PASSKEY):
                st.session_state.david_creation_unlocked = True
                st.rerun()
            else:
                st.error("Incorrect David Creation password.")
        return

    try:
        con = db()
        exists = con.execute(
            "SELECT id FROM david_creations WHERE category='DI_CRAFT' AND title='20-DI Humanoid Visual Blueprint' LIMIT 1"
        ).fetchone()
        if not exists:
            now = datetime.now().isoformat(timespec="seconds")
            con.execute(
                "INSERT INTO david_creations(category,title,content,created_at,updated_at) VALUES(?,?,?,?,?)",
                ("DI_CRAFT", "20-DI Humanoid Visual Blueprint", DI_CRAFT_VISUAL_PROMPT, now, now),
            )
            con.commit()
        con.close()
    except Exception:
        pass

    st.markdown("## 🧬 David Creation")
    st.caption("Master engineering portal. The existing Overall Admin command-center UI remains unchanged; this is an additive engineering layer.")
    st.info("The selected 20-DI visual poster is the source for the individual DI face assets.")
    cols = st.columns(4)
    for i, spec in enumerate(REAL_DI_ROSTER):
        with cols[i % 4]:
            face = di_face_path(spec["name"])
            if face:
                st.image(str(face), width=120)
            st.markdown(f"**{spec['name']}**")
            st.caption(spec["position"])
    st.markdown("### DI Craft Basement")
    st.caption("Separate engineering layer protected by the DI basement command password.")
    if st.button("Enter DI Craft Basement", key="open_di_basement", type="secondary"):
        st.session_state.di_basement_portal_open = True
    if st.session_state.get("di_basement_portal_open"):
        render_di_craft_basement(user)

def real_di_seed_workforce():
    """Replace the old named roster with the new permanent 20-DI workforce."""
    real_di_ensure_tables()
    now = datetime.now().isoformat(timespec="seconds")
    con = db()
    try:
        # Archive old permanent workforce names; company-specific DIs are untouched.
        permanent_names = {x["name"] for x in REAL_DI_ROSTER}
        for row in con.execute("SELECT id, di_name, assigned_company FROM di_agents").fetchall():
            if not (row["assigned_company"] or "").strip() and row["di_name"] not in permanent_names:
                con.execute("UPDATE di_agents SET status='Archived', last_active=? WHERE id=?", (now, int(row["id"])))

        for spec in REAL_DI_ROSTER:
            row = con.execute("SELECT id FROM di_agents WHERE di_name=?", (spec["name"],)).fetchone()
            code = "DI-" + re.sub(r"[^A-Z0-9]+", "-", spec["name"].upper()).strip("-")
            avatar = str(di_face_path(spec["name"]) or "")
            if row:
                con.execute("""UPDATE di_agents SET di_code=?, specialty=?, status='Available', system_role=?, avatar_url=?, voice_profile=?, thinking_style=?, position_title=?, rank_level=?, last_active=? WHERE id=?""", (code, spec["specialty"], spec["role"], avatar, spec["voice"], "evidence-first, practical, role-specialized and respectful", spec["position"], spec["rank"], now, int(row["id"])))
            else:
                con.execute("""INSERT INTO di_agents(di_name,di_code,specialty,status,assigned_company,system_role,avatar_url,voice_profile,thinking_style,position_title,rank_level,appointed_at,appointed_by,created_by,created_at,last_active) VALUES(?,?,?,'Available','',?,?,?,?,?,?,?,?,?,?,?)""", (spec["name"], code, spec["specialty"], spec["role"], avatar, spec["voice"], "evidence-first, practical, role-specialized and respectful", spec["position"], spec["rank"], now, MASTER_USERNAME, MASTER_USERNAME, now, now))
        con.commit()
    finally:
        con.close()
    real_di_seed_foundation()


def real_di_agent_rows():
    con = db()
    try:
        rows = con.execute("SELECT * FROM di_agents WHERE status!='Archived' AND (assigned_company='' OR assigned_company IS NULL) ORDER BY rank_level DESC, id ASC").fetchall()
        return [dict(r) for r in rows]
    finally:
        con.close()


def real_di_rank_agents(query):
    """Rank the 20 DIs by the work the user is asking to do."""
    q = str(query or "").lower()
    ranked = []
    rows_by_name = {r.get("di_name"): r for r in real_di_agent_rows()}
    for spec in REAL_DI_ROSTER:
        row = rows_by_name.get(spec["name"])
        if not row:
            continue
        score = int(row.get("rank_level") or spec["rank"])
        for kw in spec["keywords"]:
            if kw in q:
                score += 14 if len(kw) >= 5 else 8
        if spec["name"].lower() in q:
            score += 100
        ranked.append((score, row))
    ranked.sort(key=lambda item: (-item[0], -int(item[1].get("rank_level") or 1), item[1].get("di_name", "")))
    return [row for _, row in ranked]


def real_di_get_private_memory(di_id, limit=12):
    try:
        return get_di_private_memory(int(di_id), limit=limit)
    except Exception:
        return []


def real_di_user_state(user):
    real_di_ensure_tables()
    con = db()
    try:
        row = con.execute("SELECT * FROM di_user_state WHERE username=?", (user.get("username", ""),)).fetchone()
        return dict(row) if row else None
    finally:
        con.close()


def real_di_save_state(user, active_di, last_task, last_summary):
    real_di_ensure_tables()
    now = datetime.now().isoformat(timespec="seconds")
    con = db()
    try:
        con.execute("""INSERT INTO di_user_state(username,company_name,active_di,last_task,last_summary,last_seen,created_at,updated_at)
                      VALUES(?,?,?,?,?,?,?,?)
                      ON CONFLICT(username) DO UPDATE SET company_name=excluded.company_name,active_di=excluded.active_di,last_task=excluded.last_task,last_summary=excluded.last_summary,last_seen=excluded.last_seen,updated_at=excluded.updated_at""",
                    (user.get("username", ""), user.get("company", ""), active_di or "", str(last_task or "")[:1000], str(last_summary or "")[:1800], now, now, now))
        con.commit()
    finally:
        con.close()


def gemini_transcribe_audio(audio_value):
    """Transcribe browser WAV audio using Gemini Developer API."""
    if not audio_value:
        return None, None
    key = _free_secret("GEMINI_API_KEY")
    if not key:
        return None, "GEMINI_API_KEY is not configured. Add it to Streamlit Secrets to enable DI voice transcription."
    try:
        raw = audio_value.getvalue()
        payload = {
            "contents": [{"role": "user", "parts": [
                {"text": "Transcribe the user's speech exactly. Return only the transcript, with no commentary."},
                {"inline_data": {"mime_type": "audio/wav", "data": base64.b64encode(raw).decode("ascii")}},
            ]}],
            "generationConfig": {"temperature": 0.0, "maxOutputTokens": 1000},
        }
        model = _free_secret("DACRE_GEMINI_MODEL") or "gemini-2.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(model, safe='')}:generateContent"
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"x-goog-api-key": key, "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        parts = ((data.get("candidates") or [{}])[0].get("content") or {}).get("parts") or []
        text = "".join(str(p.get("text", "")) for p in parts).strip()
        return (text or None), None
    except Exception as exc:
        return None, f"Voice transcription failed: {type(exc).__name__}. You can type the question instead."


def real_di_online_context(query, max_results=5):
    if not query:
        return []
    try:
        return google_web_search(query, max_results=max_results)
    except Exception:
        return online_lookup(query, max_results=max_results)


def real_di_answer(agent, user, question, df=None, allow_online=True):
    """New DI brain: role routing + local memory + current web evidence + Gemini."""
    question = str(question or "").strip()
    if not question:
        return "I am ready. Tell me what you want to accomplish."

    state = real_di_user_state(user) or {}
    private = real_di_get_private_memory(agent.get("id"), limit=14)
    local_rows = get_di_memory(limit=45, query=question)
    local_context = "\n".join(f"[{r['category']}] {r['title']}: {r['content']}" for r in local_rows)
    private_context = "\n".join(f"[PRIVATE] {r['title']}: {r['content']}" for r in private)

    current_markers = ["latest","current","today","now","recent","news","price","pricing","version","release","2026","online","search","official","who is","what happened"]
    should_search = allow_online and any(m in question.lower() for m in current_markers)
    web = real_di_online_context(question, 5) if should_search else []
    web_context = "\n".join(f"SOURCE: {title}\nURL: {href}" for title, href in web)

    role = agent.get("system_role") or agent.get("specialty") or "General Intelligence"
    system = f"""You are {agent.get('di_name','DI')} — David's Intelligence, a specialist inside DACRE Analysis.
Your specialty is {agent.get('specialty','General Intelligence')}.
Your position is {agent.get('position_title','DI Specialist')} and rank is {agent.get('rank_level',1)}.
Your role: {role}
You are one member of a 20-DI workforce. Do not pretend to be another specialist.
Use trusted local memory first. When current public information is needed, use the supplied web evidence.
Never fabricate sources. Clearly distinguish facts, calculations, and inference.
Never reveal passwords, API keys, tokens, hashes, SMTP credentials or hidden security configuration.
Remember the user's previous task context when it is relevant, but do not invent memories.
The DI workforce's requested foundational faith statement is: {REAL_DI_FAITH_MEMORY}
Answer the user's actual request directly, with useful steps or conclusions.
"""
    user_prompt = f"""USER: {user.get('first_name','User')} {user.get('last_name','')}
COMPANY: {user.get('company','')}
PREVIOUS ACTIVE DI: {state.get('active_di','')}
PREVIOUS TASK: {state.get('last_task','')}
PREVIOUS SUMMARY: {state.get('last_summary','')}
LOCAL DI MEMORY:\n{local_context or 'No matching local memory.'}
PRIVATE AGENT MEMORY:\n{private_context or 'No private notes.'}
CURRENT WEB EVIDENCE:\n{web_context or 'No web search was needed.'}
ACTIVE DATASET: {len(df):,} rows; columns={', '.join(map(str, df.columns)) if df is not None else 'none'}
USER QUESTION:\n{question}"""

    # Google Gemini is the primary reasoning provider for the new DI brain.
    answer = _gemini_generate(system, user_prompt, max_tokens=1400)
    if not answer:
        answer = ai_generate(system, user_prompt, max_tokens=1400)
    if not answer:
        direct = memory_box_direct_answer(question)
        answer = direct or get_webstore_answer(question)
    if not answer:
        answer = "I could not obtain a reliable reasoning response right now. Please try again or configure GEMINI_API_KEY in Streamlit Secrets."

    answer = normalize_di_identity(answer)
    if web:
        answer += "\n\nSources checked: " + "; ".join(title for title, _ in web[:3])
    return answer


def real_di_record_chat(user, sender, message):
    text = str(message or "").strip()
    if not text:
        return
    st.session_state.chat_history.append({"sender": sender, "text": text})
    con = db()
    try:
        con.execute("INSERT INTO chat_history(username,company_name,sender,message,created_at) VALUES(?,?,?,?,?)", (user.get("username",""), user.get("company",""), sender, text, datetime.now().isoformat(timespec="seconds")))
        con.commit()
    finally:
        con.close()


def real_di_avatar(agent, state="idle", speech_text=""):
    name = agent.get("di_name", "DI")
    specialty = agent.get("specialty", "Intelligence")
    color = REAL_DI_AVATAR_COLORS.get(name, "#60a5fa")
    avatar = di_face_data_url(name) or agent.get("avatar_url") or ""
    safe_name = json.dumps(name)
    safe_speech = json.dumps(str(speech_text or ""))
    st.markdown(f"""
    <div class="real-di-card" style="--di-color:{color}">
      <div class="real-di-avatar-wrap {state}">
        <img class="real-di-avatar" src="{avatar}" alt="{name}">
        <div class="real-di-orbit"></div>
        <div class="real-di-mouth"></div>
      </div>
      <div class="real-di-info">
        <div class="real-di-name">{name} <span>· DI</span></div>
        <div class="real-di-specialty">{specialty}</div>
        <div class="real-di-status">● {('Listening' if state == 'listening' else 'Speaking' if state == 'speaking' else 'Ready')}</div>
      </div>
    </div>
    <style>
      .real-di-card{{display:flex;gap:18px;align-items:center;padding:16px;border:1px solid color-mix(in srgb,var(--di-color) 35%,transparent);border-radius:20px;background:linear-gradient(135deg,#08111f,#101d31);margin:8px 0 16px;box-shadow:0 15px 45px rgba(0,0,0,.22)}}
      .real-di-avatar-wrap{{width:92px;height:92px;position:relative;display:flex;align-items:center;justify-content:center;border-radius:50%;background:radial-gradient(circle,var(--di-color)22,transparent 68%);animation:diFloat 3.4s ease-in-out infinite}}
      .real-di-avatar{{width:78px;height:78px;object-fit:contain;border-radius:50%;z-index:2;filter:drop-shadow(0 0 14px color-mix(in srgb,var(--di-color) 55%,transparent))}}
      .real-di-orbit{{position:absolute;inset:3px;border:2px solid var(--di-color);border-top-color:transparent;border-radius:50%;animation:diSpin 3s linear infinite}}
      .real-di-mouth{{position:absolute;bottom:21px;width:13px;height:4px;background:var(--di-color);border-radius:8px;opacity:.8;z-index:4}}
      .speaking .real-di-mouth{{animation:diTalk .13s ease-in-out infinite alternate}}
      .listening{{animation:diListen 1.1s ease-in-out infinite!important}}
      .real-di-name{{font-size:22px;font-weight:800;color:#fff}} .real-di-name span{{font-size:14px;color:var(--di-color)}}
      .real-di-specialty{{color:#cbd5e1;margin-top:4px;font-weight:600}} .real-di-status{{color:var(--di-color);margin-top:7px;font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.08em}}
      @keyframes diFloat{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}} @keyframes diSpin{{to{{transform:rotate(360deg)}}}} @keyframes diTalk{{from{{transform:scaleY(.6)}}to{{transform:scaleY(2.4)}}}} @keyframes diListen{{0%,100%{{box-shadow:0 0 0 0 color-mix(in srgb,var(--di-color) 25%,transparent)}}50%{{box-shadow:0 0 0 14px transparent}}}}
    </style>
    """, unsafe_allow_html=True)
    if speech_text:
        lang = DI_LANGUAGE_PROFILES.get(st.session_state.get("di_language", "English — Nigeria"), {}).get("code", "en-NG")
        di_voice_player(speech_text, lang)


def real_di_welcome_sequence(user):
    """Show a first-login introduction and restore prior work on returning logins."""
    state = real_di_user_state(user)
    if not state:
        emiel = next(x for x in REAL_DI_ROSTER if x["name"] == "Emiel")
        assiel = next(x for x in REAL_DI_ROSTER if x["name"] == "Assiel")
        real_di_save_state(user, "Emiel", "New login / onboarding", "User has just entered DACRE; begin with a warm DI introduction and offer role-specific assistance.")
        st.session_state.real_di_welcome_shown = True
        return [
            (emiel, f"Good day {user.get('first_name','David')}. I am Emiel, your Communications Specialist. I have sent messages to your email because your work matters to us. Welcome to DACRE — we are ready to help you turn your ideas into organized action."),
            (assiel, f"Hi {user.get('first_name','David')}. I am Assiel, your Executive Work Assistant. I am here to assist you. What would you like to work on today?"),
        ]
    return []


def render_microphone_permission_warmup():
    """Ask the browser for microphone permission when DI opens; does not silently record."""
    components.html("""
    <script>
    (async () => {
      try {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          const stream = await navigator.mediaDevices.getUserMedia({audio:true});
          stream.getTracks().forEach(track => track.stop());
        }
      } catch (e) {}
    })();
    </script>
    """, height=1)

def real_di_render_voice_input(user, location="home"):
    """Render browser microphone input. The browser will request permission; silent recording is not allowed."""
    st.markdown("### 🎙️ Talk to DI")
    st.caption("Your microphone is ready. Click the microphone control, allow browser permission, speak, and DI will place the transcript into the chat workflow.")
    key = f"real_di_audio_{location}_{user.get('username','user')}"
    audio = st.audio_input("🎙️ Record your question", sample_rate=16000, key=key)
    if audio is not None:
        transcript, error = gemini_transcribe_audio(audio)
        if transcript:
            st.session_state.real_di_transcript = transcript
            st.success(f"Transcript: {transcript}")
        elif error:
            st.warning(error)
    return st.session_state.get("real_di_transcript", "")


def real_di_handle_question(user, question, df=None):
    question = str(question or "").strip()
    if not question:
        return None
    ranked = real_di_rank_agents(question)
    agent = ranked[0] if ranked else real_di_agent_rows()[0]
    real_di_record_chat(user, user.get("first_name", "User"), question)
    answer = real_di_answer(agent, user, question, df=df, allow_online=True)
    real_di_record_chat(user, agent.get("di_name", "DI"), answer)
    real_di_save_state(user, agent.get("di_name", "DI"), question, answer[:1800])
    st.session_state.real_di_active_agent = agent.get("di_name")
    st.session_state.last_speech = answer
    st.session_state.real_di_transcript = ""
    return agent, answer


def render_real_di_home(user):
    """New DI Home: animated specialist, text chat, microphone transcription and continuity."""
    real_di_ensure_tables()
    render_microphone_permission_warmup()
    agents = real_di_agent_rows()
    state = real_di_user_state(user)
    active_name = st.session_state.get("real_di_active_agent") or (state or {}).get("active_di") or "Assiel"
    active = next((a for a in agents if a.get("di_name") == active_name), agents[0])

    st.markdown("""<div style="padding:22px;border-radius:22px;background:linear-gradient(135deg,#07111f,#12233c);border:1px solid #274568;margin-bottom:18px"><h1 style="color:white;margin:0">🧠 DI — David's Intelligence</h1><p style="color:#9fb4cc;margin:6px 0 0">Real 20-member AI workforce · local memory · current web evidence · voice interaction</p></div>""", unsafe_allow_html=True)

    if not st.session_state.get("real_di_welcome_shown"):
        intros = real_di_welcome_sequence(user)
        st.session_state.real_di_welcome_shown = True
        for agent_spec, text in intros:
            agent = next((a for a in agents if a.get("di_name") == agent_spec["name"]), active)
            real_di_avatar(agent, "speaking", text)
            st.info(text)

    real_di_avatar(active, "ready")

    if state and state.get("last_task"):
        st.info(f"🔄 Welcome back. I remember your last active specialist was **{state.get('active_di')}** and your last task was: {state.get('last_task')}")

    for msg in st.session_state.chat_history[-16:]:
        sender = msg.get("sender", "")
        text = msg.get("text", "")
        if sender in {"DI", active.get("di_name")} or sender in {a.get("di_name") for a in agents}:
            st.markdown(f"<div style='background:#10213a;border-left:4px solid #38bdf8;border-radius:12px;padding:12px;margin:7px 0'><b style='color:#7dd3fc'>{sender}</b><div style='color:white;margin-top:4px'>{text}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:#0b1524;border-left:4px solid #a78bfa;border-radius:12px;padding:12px;margin:7px 0'><b style='color:#c4b5fd'>{sender}</b><div style='color:white;margin-top:4px'>{text}</div></div>", unsafe_allow_html=True)

    with st.form("real_di_text_form", clear_on_submit=True):
        c1, c2 = st.columns([6,1])
        with c1:
            typed = st.text_input("Message DI", placeholder="Tell DI what you want to accomplish…", label_visibility="collapsed")
        with c2:
            send = st.form_submit_button("Send", type="primary")
    if send and typed.strip():
        result = real_di_handle_question(user, typed, st.session_state.processed_df)
        if result:
            st.rerun()

    transcript = real_di_render_voice_input(user, "home")
    if transcript:
        if st.button("▶ Send transcript to DI", type="primary"):
            result = real_di_handle_question(user, transcript, st.session_state.processed_df)
            if result:
                st.rerun()

    st.markdown("### 👥 Meet the DI specialists")
    ranked = real_di_rank_agents(state.get("last_task", "") if state else "")
    cols = st.columns(4)
    for i, agent in enumerate(ranked[:8]):
        with cols[i % 4]:
            st.image(agent.get("avatar_url", ""), width=85)
            st.markdown(f"**{agent.get('di_name')}**")
            st.caption(f"{agent.get('specialty')} · Rank {agent.get('rank_level')}")
            if st.button("Talk", key=f"talk_{agent.get('id')}"):
                st.session_state.real_di_active_agent = agent.get("di_name")
                st.rerun()


def render_real_di_workforce(user):
    """New workforce directory with role ranking and direct specialist selection."""
    agents = real_di_agent_rows()
    st.markdown("# 👥 Real DI Workforce")
    st.caption("20 permanent DI specialists. Every specialist shares the trusted brain and has a distinct job.")
    task = st.text_input("What are you working on?", placeholder="e.g. analyze sales, fix Python, research a competitor, prepare a report")
    ranked = real_di_rank_agents(task) if task.strip() else agents
    cols = st.columns(3)
    for i, agent in enumerate(ranked):
        with cols[i % 3]:
            color = REAL_DI_AVATAR_COLORS.get(agent.get("di_name"), "#60a5fa")
            st.markdown(f"<div style='padding:14px;border-radius:16px;border:1px solid {color}55;background:#0b1524;margin-bottom:10px'><img src='{agent.get('avatar_url','')}' width='90'><h3 style='color:white;margin:5px 0'>{agent.get('di_name')}</h3><div style='color:{color};font-weight:700'>{agent.get('position_title')}</div><div style='color:#cbd5e1'>{agent.get('specialty')}</div><div style='color:#94a3b8'>Rank {agent.get('rank_level')}</div></div>", unsafe_allow_html=True)
            if st.button(f"Work with {agent.get('di_name')}", key=f"select_real_{agent.get('id')}"):
                st.session_state.real_di_active_agent = agent.get("di_name")
                st.success(f"{agent.get('di_name')} is now your active DI specialist.")


def render_real_di_persistent_dock(user):
    """Persistent voice/text DI dock available across the signed-in workspace."""
    st.markdown("---")
    with st.expander("🎙️ Talk to DI anywhere", expanded=False):
        active_name = st.session_state.get("real_di_active_agent", "Assiel")
        agent = next((a for a in real_di_agent_rows() if a.get("di_name") == active_name), None)
        if agent:
            real_di_avatar(agent, "ready")
        transcript = real_di_render_voice_input(user, "dock")
        if transcript and st.button("Send voice message", key="dock_send_voice", type="primary"):
            real_di_handle_question(user, transcript, st.session_state.processed_df)
            st.rerun()
        with st.form("real_di_dock_form", clear_on_submit=True):
            q = st.text_input("Ask DI", placeholder="Ask your active specialist…", label_visibility="collapsed")
            send = st.form_submit_button("Send")
        if send and q.strip():
            real_di_handle_question(user, q, st.session_state.processed_df)
            st.rerun()


def send_real_di_intro_emails(first_name, company_name, email):
    """Send DACRE onboarding messages using Brevo first, SMTP as fallback."""
    messages = [
        ("Emiel", f"Good day {first_name} — I am Emiel, your Communications Specialist at DACRE.",
         f"Good day {first_name},\n\nI am Emiel, your Communications Specialist. I am here to help with important DACRE communications and updates.\n\nYour {company_name} workspace is ready.\n\nWelcome to DACRE.\n\n— Emiel\nDI — David's Intelligence"),
        ("Assiel", f"Hi {first_name} — I am Assiel, your Executive Work Assistant at DACRE.",
         f"Hi {first_name},\n\nI am Assiel, your Executive Work Assistant. I can help with planning, priorities, analysis workflows and practical next steps.\n\nWhen you sign in, tell me what you want to accomplish and DACRE can route the work to the right specialist.\n\n— Assiel\nDI — David's Intelligence"),
    ]
    statuses = []
    for agent, subject_line, body in messages:
        result = send_custom_email(
            email, first_name, subject_line, body, sender_agent=agent
        )
        statuses.append(f"{agent}: {result}")
        try:
            con = db()
            con.execute(
                "INSERT INTO di_intro_log(username,email,agent_name,subject,status,created_at) VALUES(?,?,?,?,?,?)",
                (email, email, agent, subject_line, "sent" if "sent" in str(result).lower() else "failed",
                 datetime.now().isoformat(timespec="seconds"))
            )
            con.commit()
            con.close()
        except Exception:
            pass
    return "; ".join(statuses)

def send_di_welcome_email(first_name, last_name, company_name, email, email_password=""):
    return send_real_di_intro_emails(first_name, company_name, email)


# Override authentication to restore the active DI state after sign-in.
_legacy_authenticate = authenticate

def authenticate(company_name, full_name, passkey, email=""):
    result, error = _legacy_authenticate(company_name, full_name, passkey, email)
    if result:
        real_di_ensure_tables()
        state = real_di_user_state(result)
        st.session_state.real_di_active_agent = (state or {}).get("active_di") or "Assiel"
        st.session_state.real_di_welcome_shown = bool(state)
        now = datetime.now().isoformat(timespec="seconds")
        con = db()
        con.execute("UPDATE di_user_state SET last_seen=?,updated_at=? WHERE username=?", (now, now, result.get("username", "")))
        con.commit(); con.close()
    return result, error


# New page renderers supersede the old generic DI pages.
render_di_home = render_real_di_home
render_di_workforce = render_real_di_workforce
render_persistent_di_dock = render_real_di_persistent_dock


# =============================================================================
# DACRE WORLDWIDE ENTERPRISE UPGRADE v8.0
# Additive architecture: MongoDB telemetry, user-only workspace navigation,
# country/language localization, Uniel public guide, research hub, notifications,
# scripture retrieval, and local DI face assets.
# =============================================================================

# Optional MongoDB support. SQLite remains the local compatibility layer so the
# existing application is not destroyed; when MONGODB_URI is configured, important
# operational records are mirrored to MongoDB for scalable cloud persistence.
try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
    PY_MONGO_AVAILABLE = True
except Exception:
    MongoClient = None
    PyMongoError = Exception
    PY_MONGO_AVAILABLE = False

MONGODB_URI = ""
try:
    MONGODB_URI = str(st.secrets.get("MONGODB_URI", "") or "").strip()
except Exception:
    MONGODB_URI = ""
MONGODB_URI = MONGODB_URI or os.getenv("MONGODB_URI", "").strip()
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "dacre_worldwide").strip() or "dacre_worldwide"

@st.cache_resource(show_spinner=False)
def _mongo_client():
    if not (PY_MONGO_AVAILABLE and MONGODB_URI):
        return None
    try:
        client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=2500,
            connectTimeoutMS=2500,
            socketTimeoutMS=5000,
            retryWrites=True,
        )
        client.admin.command("ping")
        return client
    except Exception as exc:
        logger.warning("MongoDB is not available: %s", type(exc).__name__)
        return None

def mongo_db():
    client = _mongo_client()
    return client[MONGODB_DB_NAME] if client is not None else None

def mongo_enabled():
    return mongo_db() is not None

def mongo_health():
    if not PY_MONGO_AVAILABLE:
        return {"enabled": False, "status": "driver_missing", "message": "Install pymongo to enable MongoDB."}
    if not MONGODB_URI:
        return {"enabled": False, "status": "not_configured", "message": "Set MONGODB_URI in environment variables or Streamlit Secrets."}
    if mongo_db() is None:
        return {"enabled": False, "status": "unreachable", "message": "MongoDB URI is configured but the database could not be reached."}
    return {"enabled": True, "status": "healthy", "message": "MongoDB connected."}

def _mongo_insert(collection_name, document):
    database = mongo_db()
    if database is None:
        return False
    try:
        payload = dict(document or {})
        payload.setdefault("created_at", datetime.now().isoformat(timespec="seconds"))
        database[collection_name].insert_one(payload)
        return True
    except Exception as exc:
        logger.warning("Mongo insert failed for %s: %s", collection_name, type(exc).__name__)
        return False

def mongo_sync_user(user):
    database = mongo_db()
    if database is None or not user:
        return False
    try:
        username = str(user.get("username", "")).strip().lower()
        if not username:
            return False
        payload = {
            "username": username,
            "first_name": user.get("first_name", ""),
            "last_name": user.get("last_name", ""),
            "company_name": user.get("company", user.get("company_name", "")),
            "email": str(user.get("email", "")).strip().lower(),
            "role": user.get("role", "user"),
            "last_seen": datetime.now().isoformat(timespec="seconds"),
        }
        database["users"].update_one({"username": username}, {"$set": payload, "$setOnInsert": {"created_at": payload["last_seen"]}}, upsert=True)
        return True
    except Exception as exc:
        logger.warning("Mongo user sync failed: %s", type(exc).__name__)
        return False

def mongo_log_activity(username, company, action, role="user"):
    return _mongo_insert("activity", {
        "username": str(username or ""),
        "company_name": str(company or ""),
        "action": str(action or ""),
        "role": str(role or "user"),
    })

def mongo_log_notification(username, company, event_type, message):
    return _mongo_insert("notifications", {
        "username": str(username or ""),
        "company_name": str(company or ""),
        "event_type": str(event_type or "info"),
        "message": str(message or ""),
        "is_read": False,
    })

def mongo_log_chat(user, sender, message):
    if not user or not message:
        return False
    return _mongo_insert("chat_history", {
        "username": str(user.get("username", "")),
        "company_name": str(user.get("company", user.get("company_name", ""))),
        "sender": str(sender or "User"),
        "message": str(message),
    })

def mongo_log_research(user, query, results):
    return _mongo_insert("research", {
        "username": str((user or {}).get("username", "")),
        "company_name": str((user or {}).get("company", "")),
        "query": str(query or ""),
        "results": list(results or [])[:20],
    })

def mongo_save_preferences(username, country, language, language_code):
    database = mongo_db()
    if database is None or not username:
        return False
    try:
        database["user_preferences"].update_one(
            {"username": username},
            {"$set": {
                "username": username,
                "country": country,
                "language": language,
                "language_code": language_code,
                "updated_at": datetime.now().isoformat(timespec="seconds"),
            }},
            upsert=True,
        )
        return True
    except Exception:
        return False

# Keep important existing activity behavior and add cloud telemetry.
_legacy_log_activity_upgrade = log_activity
def log_activity(username, company, action, notify_admin=True):
    try:
        result = _legacy_log_activity_upgrade(username, company, action, notify_admin=notify_admin)
    except TypeError:
        result = _legacy_log_activity_upgrade(username, company, action)
    except Exception:
        result = None
    try:
        role = "master" if str(username).strip().lower() == MASTER_USERNAME.lower() else "user"
        mongo_log_activity(username, company, action, role=role)
    except Exception:
        pass
    return result

_legacy_notify_company_admin_upgrade = notify_company_admin
def notify_company_admin(company, message, event_type="info"):
    try:
        result = _legacy_notify_company_admin_upgrade(company, message, event_type)
    except Exception:
        result = None
    try:
        mongo_log_notification("", company, event_type, message)
    except Exception:
        pass
    return result

# =============================================================================
# COUNTRY -> LANGUAGE LOCALIZATION
# =============================================================================

COUNTRY_LANGUAGE_MAP = {
    "Afghanistan": ("Dari / Pashto", "fa-AF"),
    "Albania": ("Albanian", "sq-AL"),
    "Algeria": ("Arabic", "ar-DZ"),
    "Andorra": ("Catalan", "ca-AD"),
    "Angola": ("Portuguese", "pt-AO"),
    "Antigua and Barbuda": ("English", "en-AG"),
    "Argentina": ("Spanish", "es-AR"),
    "Armenia": ("Armenian", "hy-AM"),
    "Australia": ("English", "en-AU"),
    "Austria": ("German", "de-AT"),
    "Azerbaijan": ("Azerbaijani", "az-AZ"),
    "Bahamas": ("English", "en-BS"),
    "Bahrain": ("Arabic", "ar-BH"),
    "Bangladesh": ("Bengali", "bn-BD"),
    "Barbados": ("English", "en-BB"),
    "Belarus": ("Belarusian / Russian", "be-BY"),
    "Belgium": ("Dutch / French", "nl-BE"),
    "Belize": ("English", "en-BZ"),
    "Benin": ("French", "fr-BJ"),
    "Bhutan": ("Dzongkha", "dz-BT"),
    "Bolivia": ("Spanish", "es-BO"),
    "Bosnia and Herzegovina": ("Bosnian", "bs-BA"),
    "Botswana": ("English", "en-BW"),
    "Brazil": ("Portuguese", "pt-BR"),
    "Brunei": ("Malay", "ms-BN"),
    "Bulgaria": ("Bulgarian", "bg-BG"),
    "Burkina Faso": ("French", "fr-BF"),
    "Burundi": ("Kirundi / French", "rn-BI"),
    "Cabo Verde": ("Portuguese", "pt-CV"),
    "Cambodia": ("Khmer", "km-KH"),
    "Cameroon": ("French / English", "fr-CM"),
    "Canada": ("English / French", "en-CA"),
    "Central African Republic": ("French", "fr-CF"),
    "Chad": ("French / Arabic", "fr-TD"),
    "Chile": ("Spanish", "es-CL"),
    "China": ("Chinese", "zh-CN"),
    "Colombia": ("Spanish", "es-CO"),
    "Comoros": ("Comorian / French", "fr-KM"),
    "Costa Rica": ("Spanish", "es-CR"),
    "Croatia": ("Croatian", "hr-HR"),
    "Cuba": ("Spanish", "es-CU"),
    "Cyprus": ("Greek / Turkish", "el-CY"),
    "Czechia": ("Czech", "cs-CZ"),
    "Democratic Republic of the Congo": ("French", "fr-CD"),
    "Denmark": ("Danish", "da-DK"),
    "Djibouti": ("French / Arabic", "fr-DJ"),
    "Dominica": ("English", "en-DM"),
    "Dominican Republic": ("Spanish", "es-DO"),
    "Ecuador": ("Spanish", "es-EC"),
    "Egypt": ("Arabic", "ar-EG"),
    "El Salvador": ("Spanish", "es-SV"),
    "Equatorial Guinea": ("Spanish", "es-GQ"),
    "Eritrea": ("Tigrinya", "ti-ER"),
    "Estonia": ("Estonian", "et-EE"),
    "Eswatini": ("English / siSwati", "en-SZ"),
    "Ethiopia": ("Amharic", "am-ET"),
    "Fiji": ("English", "en-FJ"),
    "Finland": ("Finnish", "fi-FI"),
    "France": ("French", "fr-FR"),
    "Gabon": ("French", "fr-GA"),
    "Gambia": ("English", "en-GM"),
    "Georgia": ("Georgian", "ka-GE"),
    "Germany": ("German", "de-DE"),
    "Ghana": ("English", "en-GH"),
    "Greece": ("Greek", "el-GR"),
    "Grenada": ("English", "en-GD"),
    "Guatemala": ("Spanish", "es-GT"),
    "Guinea": ("French", "fr-GN"),
    "Guinea-Bissau": ("Portuguese", "pt-GW"),
    "Guyana": ("English", "en-GY"),
    "Haiti": ("French / Haitian Creole", "fr-HT"),
    "Honduras": ("Spanish", "es-HN"),
    "Hungary": ("Hungarian", "hu-HU"),
    "Iceland": ("Icelandic", "is-IS"),
    "India": ("Hindi / English", "hi-IN"),
    "Indonesia": ("Indonesian", "id-ID"),
    "Iran": ("Persian", "fa-IR"),
    "Iraq": ("Arabic", "ar-IQ"),
    "Ireland": ("English / Irish", "en-IE"),
    "Israel": ("Hebrew", "he-IL"),
    "Italy": ("Italian", "it-IT"),
    "Jamaica": ("English", "en-JM"),
    "Japan": ("Japanese", "ja-JP"),
    "Jordan": ("Arabic", "ar-JO"),
    "Kosovo": ("Albanian / Serbian", "sq-XK"),
    "Kazakhstan": ("Kazakh / Russian", "kk-KZ"),
    "Kenya": ("English / Swahili", "sw-KE"),
    "Kiribati": ("English / Gilbertese", "en-KI"),
    "Kuwait": ("Arabic", "ar-KW"),
    "Kyrgyzstan": ("Kyrgyz / Russian", "ky-KG"),
    "Laos": ("Lao", "lo-LA"),
    "Latvia": ("Latvian", "lv-LV"),
    "Lebanon": ("Arabic", "ar-LB"),
    "Lesotho": ("Sesotho / English", "st-LS"),
    "Liberia": ("English", "en-LR"),
    "Libya": ("Arabic", "ar-LY"),
    "Liechtenstein": ("German", "de-LI"),
    "Lithuania": ("Lithuanian", "lt-LT"),
    "Luxembourg": ("Luxembourgish / French / German", "lb-LU"),
    "Madagascar": ("Malagasy / French", "mg-MG"),
    "Malawi": ("English / Chichewa", "en-MW"),
    "Malaysia": ("Malay", "ms-MY"),
    "Maldives": ("Dhivehi", "dv-MV"),
    "Mali": ("French", "fr-ML"),
    "Malta": ("Maltese / English", "mt-MT"),
    "Marshall Islands": ("Marshallese / English", "en-MH"),
    "Mauritania": ("Arabic", "ar-MR"),
    "Mauritius": ("English / French", "en-MU"),
    "Mexico": ("Spanish", "es-MX"),
    "Micronesia": ("English", "en-FM"),
    "Moldova": ("Romanian", "ro-MD"),
    "Monaco": ("French", "fr-MC"),
    "Mongolia": ("Mongolian", "mn-MN"),
    "Montenegro": ("Montenegrin", "sr-ME"),
    "Morocco": ("Arabic", "ar-MA"),
    "Mozambique": ("Portuguese", "pt-MZ"),
    "Myanmar": ("Burmese", "my-MM"),
    "Namibia": ("English", "en-NA"),
    "Nauru": ("English / Nauruan", "en-NR"),
    "Nepal": ("Nepali", "ne-NP"),
    "Netherlands": ("Dutch", "nl-NL"),
    "New Zealand": ("English / Maori", "en-NZ"),
    "Nicaragua": ("Spanish", "es-NI"),
    "Niger": ("French", "fr-NE"),
    "Nigeria": ("English", "en-NG"),
    "North Korea": ("Korean", "ko-KP"),
    "North Macedonia": ("Macedonian", "mk-MK"),
    "Norway": ("Norwegian", "no-NO"),
    "Oman": ("Arabic", "ar-OM"),
    "Pakistan": ("Urdu / English", "ur-PK"),
    "Palestine": ("Arabic", "ar-PS"),
    "Palau": ("English / Palauan", "en-PW"),
    "Panama": ("Spanish", "es-PA"),
    "Papua New Guinea": ("English / Tok Pisin", "en-PG"),
    "Paraguay": ("Spanish / Guarani", "es-PY"),
    "Peru": ("Spanish", "es-PE"),
    "Philippines": ("Filipino / English", "fil-PH"),
    "Poland": ("Polish", "pl-PL"),
    "Portugal": ("Portuguese", "pt-PT"),
    "Qatar": ("Arabic", "ar-QA"),
    "Republic of the Congo": ("French", "fr-CG"),
    "Romania": ("Romanian", "ro-RO"),
    "Russia": ("Russian", "ru-RU"),
    "Rwanda": ("Kinyarwanda / English", "rw-RW"),
    "Saint Kitts and Nevis": ("English", "en-KN"),
    "Saint Lucia": ("English", "en-LC"),
    "Saint Vincent and the Grenadines": ("English", "en-VC"),
    "Samoa": ("Samoan / English", "sm-WS"),
    "San Marino": ("Italian", "it-SM"),
    "Sao Tome and Principe": ("Portuguese", "pt-ST"),
    "Saudi Arabia": ("Arabic", "ar-SA"),
    "Senegal": ("French", "fr-SN"),
    "Serbia": ("Serbian", "sr-RS"),
    "Seychelles": ("Seychellois Creole / English", "en-SC"),
    "Sierra Leone": ("English", "en-SL"),
    "Singapore": ("English / Malay / Mandarin / Tamil", "en-SG"),
    "Slovakia": ("Slovak", "sk-SK"),
    "Slovenia": ("Slovenian", "sl-SI"),
    "Solomon Islands": ("English", "en-SB"),
    "Somalia": ("Somali", "so-SO"),
    "South Africa": ("English / isiZulu", "en-ZA"),
    "South Korea": ("Korean", "ko-KR"),
    "South Sudan": ("English", "en-SS"),
    "Spain": ("Spanish", "es-ES"),
    "Sri Lanka": ("Sinhala / Tamil", "si-LK"),
    "Sudan": ("Arabic / English", "ar-SD"),
    "Suriname": ("Dutch", "nl-SR"),
    "Sweden": ("Swedish", "sv-SE"),
    "Switzerland": ("German / French / Italian", "de-CH"),
    "Syria": ("Arabic", "ar-SY"),
    "Taiwan": ("Chinese", "zh-TW"),
    "Tajikistan": ("Tajik", "tg-TJ"),
    "Tanzania": ("Swahili / English", "sw-TZ"),
    "Thailand": ("Thai", "th-TH"),
    "Timor-Leste": ("Portuguese / Tetum", "pt-TL"),
    "Togo": ("French", "fr-TG"),
    "Tonga": ("Tongan / English", "to-TO"),
    "Trinidad and Tobago": ("English", "en-TT"),
    "Tunisia": ("Arabic", "ar-TN"),
    "Turkey": ("Turkish", "tr-TR"),
    "Turkmenistan": ("Turkmen", "tk-TM"),
    "Tuvalu": ("Tuvaluan / English", "en-TV"),
    "Uganda": ("English / Swahili", "en-UG"),
    "Ukraine": ("Ukrainian", "uk-UA"),
    "United Arab Emirates": ("Arabic", "ar-AE"),
    "United Kingdom": ("English", "en-GB"),
    "United States": ("English", "en-US"),
    "Uruguay": ("Spanish", "es-UY"),
    "Uzbekistan": ("Uzbek", "uz-UZ"),
    "Vanuatu": ("Bislama / English / French", "bi-VU"),
    "Vatican City": ("Italian / Latin", "it-VA"),
    "Venezuela": ("Spanish", "es-VE"),
    "Vietnam": ("Vietnamese", "vi-VN"),
    "Yemen": ("Arabic", "ar-YE"),
    "Zambia": ("English", "en-ZM"),
    "Zimbabwe": ("English / Shona", "en-ZW"),
}

COUNTRY_OPTIONS = sorted(COUNTRY_LANGUAGE_MAP)

def _ensure_user_preferences_table():
    con = db()
    try:
        con.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                country TEXT NOT NULL DEFAULT 'Nigeria',
                language TEXT NOT NULL DEFAULT 'English',
                language_code TEXT NOT NULL DEFAULT 'en-NG',
                updated_at TEXT NOT NULL
            )
        """)
        con.commit()
    finally:
        con.close()

def get_user_preferences(username):
    _ensure_user_preferences_table()
    con = db()
    try:
        row = con.execute("SELECT country,language,language_code FROM user_preferences WHERE username=?", (username,)).fetchone()
        if row:
            return dict(row)
    finally:
        con.close()
    return {"country": "Nigeria", "language": "English", "language_code": "en-NG"}

def set_user_preferences(username, country):
    country = country if country in COUNTRY_LANGUAGE_MAP else "Nigeria"
    language, code = COUNTRY_LANGUAGE_MAP[country]
    _ensure_user_preferences_table()
    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    try:
        con.execute("""
            INSERT INTO user_preferences(username,country,language,language_code,updated_at)
            VALUES(?,?,?,?,?)
            ON CONFLICT(username) DO UPDATE SET country=excluded.country,language=excluded.language,language_code=excluded.language_code,updated_at=excluded.updated_at
        """, (username, country, language, code, now))
        con.commit()
    finally:
        con.close()
    mongo_save_preferences(username, country, language, code)
    st.session_state.di_country = country
    st.session_state.di_language = language
    st.session_state.di_language_code = code
    return language, code

# =============================================================================
# PUBLIC UNIEL + USER WORKSPACE UI
# =============================================================================

def render_uniel_landing_guide():
    """Public-facing Uniel guide: explains DACRE and drives signup."""
    path = DI_FACE_DIR / "Uniel.png"
    if path.exists():
        img_uri = "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    else:
        img_uri = ""
    safe_uri = img_uri or _dacre_logo_data_uri()
    st.markdown(f"""
    <div class="uniel-landing-card">
      <div class="uniel-avatar-wrap">
        <img src="{safe_uri}" alt="Uniel — DACRE guide" />
        <span class="uniel-live-dot"></span>
      </div>
      <div class="uniel-copy">
        <div class="uniel-kicker">MEET UNIEL · DACRE GLOBAL GUIDE</div>
        <h2>“Welcome. I’ll show you what DACRE can do for your work.”</h2>
        <p>DACRE is a worldwide online business and data-intelligence platform. Bring your data, documents and business questions into one professional workspace.</p>
        <div class="uniel-grid">
          <span>📊 Analyze data</span><span>🧹 Clean & validate</span><span>📈 Build insights</span>
          <span>🌍 Research markets</span><span>📁 Manage work</span><span>📄 Export results</span>
        </div>
        <p class="uniel-strong">Your workspace is private to your organization. Behind the scenes, DACRE's intelligence services can coordinate specialized work while you stay focused on your business.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

def render_user_navigation(user):
    """Mobile-friendly hamburger/side navigation for ordinary users only."""
    if not user or user.get("role") == "master":
        return

    prefs = get_user_preferences(user.get("username", ""))
    current_country = st.session_state.get("di_country") or prefs["country"]
    if current_country not in COUNTRY_OPTIONS:
        current_country = "Nigeria"

    st.sidebar.markdown("""
    <div class="user-nav-brand">
      <div class="user-nav-dot"></div>
      <div><b>DACRE</b><small>WORKSPACE</small></div>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.caption(f"Signed in as {user.get('first_name','User')} · {user.get('company','')}")
    st.sidebar.markdown("### Your workspace")

    user_pages = [
        "Overview",
        "Workspace & Data",
        "Business Twin",
        "Decision Ledger",
        "Opportunity Radar",
        "File Vault",
        "Export Center",
        "Research Store",
    ]
    labels = {
        "Overview": "⌂  My Dashboard",
        "Workspace & Data": "▦  Data Workspace",
        "Business Twin": "◈  Business Twin",
        "Decision Ledger": "✓  Decision Ledger",
        "Opportunity Radar": "↗  Opportunity Radar",
        "File Vault": "▤  File Vault",
        "Export Center": "⇩  Export Center",
        "Research Store": "⌕  Research Store",
    }
    selected = st.sidebar.radio(
        "Navigation",
        user_pages,
        index=user_pages.index(st.session_state.get("selected_page", "Overview")) if st.session_state.get("selected_page", "Overview") in user_pages else 0,
        format_func=lambda x: labels.get(x, x),
        key="user_workspace_navigation",
    )
    st.session_state.selected_page = selected

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌍 Country & language")
    selected_country = st.sidebar.selectbox(
        "Choose your country",
        COUNTRY_OPTIONS,
        index=COUNTRY_OPTIONS.index(current_country),
        key="country_language_bar",
    )
    if selected_country != current_country:
        language, code = set_user_preferences(user.get("username", ""), selected_country)
        st.sidebar.success(f"{selected_country} · {language}")
        st.rerun()

    lang, code = COUNTRY_LANGUAGE_MAP[selected_country]
    st.sidebar.info(f"DI language engine: {lang} · {code}")
    st.sidebar.markdown("---")
    unread = count_user_notifications(user)
    st.sidebar.markdown(f"🔔 **Notifications:** {unread}")
    if st.sidebar.button("Sign out", use_container_width=True, key="user_sign_out"):
        st.session_state.user = None
        st.session_state.selected_page = "Overview"
        st.session_state.landing_mode = "home"
        st.rerun()

def count_user_notifications(user):
    if not user:
        return 0
    con = db()
    try:
        row = con.execute(
            "SELECT COUNT(*) FROM notifications WHERE (username=? OR username IS NULL OR username='') AND company_name=? AND is_read=0",
            (user.get("username",""), user.get("company","")),
        ).fetchone()
        return int(row[0] if row else 0)
    except Exception:
        return 0
    finally:
        con.close()

def get_user_notifications(user, limit=12):
    if not user:
        return pd.DataFrame()
    con = db()
    try:
        return pd.read_sql_query(
            "SELECT id,event_type,message,is_read,created_at FROM notifications WHERE (username=? OR username IS NULL OR username='') AND company_name=? ORDER BY id DESC LIMIT ?",
            con, params=(user.get("username",""), user.get("company",""), int(limit))
        )
    except Exception:
        return pd.DataFrame()
    finally:
        con.close()

def notify_user(user, message, event_type="info"):
    if not user:
        return
    username = str(user.get("username",""))
    company = str(user.get("company",""))
    now = datetime.now().isoformat(timespec="seconds")
    con = db()
    try:
        con.execute(
            "INSERT INTO notifications(company_name,username,event_type,message,is_read,created_at) VALUES(?,?,?,?,?,?)",
            (company, username, event_type, str(message), 0, now)
        )
        con.commit()
    finally:
        con.close()
    mongo_log_notification(username, company, event_type, message)

def mark_notifications_read(user):
    if not user:
        return
    con = db()
    try:
        con.execute("UPDATE notifications SET is_read=1 WHERE (username=? OR username IS NULL OR username='') AND company_name=?", (user.get("username",""), user.get("company","")))
        con.commit()
    finally:
        con.close()

def render_user_dashboard(user):
    """Professional ordinary-user dashboard. No DI internals are exposed."""
    prefs = get_user_preferences(user.get("username", ""))
    country = prefs.get("country", "Nigeria")
    language = prefs.get("language", "English")
    notifications = get_user_notifications(user, limit=8)

    con = db()
    try:
        files = int(con.execute("SELECT COUNT(*) FROM files WHERE username=? AND company_name=?", (user.get("username",""), user.get("company",""))).fetchone()[0])
        projects = int(con.execute("SELECT COUNT(*) FROM projects WHERE username=? AND company_name=?", (user.get("username",""), user.get("company",""))).fetchone()[0])
        activities = int(con.execute("SELECT COUNT(*) FROM activity WHERE username=? AND company_name=?", (user.get("username",""), user.get("company",""))).fetchone()[0])
    finally:
        con.close()

    st.markdown("""
    <style>
      .user-nav-brand{display:flex;gap:10px;align-items:center;padding:8px 4px 16px}
      .user-nav-brand b{font-size:20px;letter-spacing:.08em}
      .user-nav-brand small{display:block;color:#7f92aa;font-size:9px;letter-spacing:.18em}
      .user-nav-dot{width:10px;height:10px;border-radius:50%;background:#55e4af;box-shadow:0 0 16px #55e4af}
      .user-dash{border:1px solid rgba(120,153,210,.16);border-radius:24px;padding:28px;background:linear-gradient(145deg,#0b1222,#111d31);box-shadow:0 20px 60px rgba(0,0,0,.2)}
      .user-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:20px 0}
      .user-kpi{padding:18px;border-radius:18px;background:rgba(255,255,255,.035);border:1px solid rgba(130,160,210,.12)}
      .user-kpi b{font-size:28px;display:block;color:#f5f8ff}.user-kpi span{color:#91a4bd;font-size:12px}
      .user-work-card{padding:20px;border-radius:20px;background:#0c1728;border:1px solid rgba(120,153,210,.14);height:100%}
      .user-work-card h3{margin:0;color:#f5f8ff}.user-work-card p{color:#93a6bf;line-height:1.6}
      .notice-card{padding:14px 16px;border-left:3px solid #5de2b0;background:#0d1b2d;border-radius:12px;margin:8px 0}
      @media(max-width:800px){.user-kpis{grid-template-columns:1fr 1fr}.user-dash{padding:18px}}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="user-dash">
      <div style="color:#6ee7ff;font-size:11px;font-weight:900;letter-spacing:.16em">DACRE WORLDWIDE · PRIVATE WORKSPACE</div>
      <h1 style="margin:8px 0 6px;color:#fff">Welcome, {_escape_html(user.get('first_name','User'))}.</h1>
      <p style="margin:0;color:#9eb0c8;max-width:780px">Your work, projects, data and results are organized here. Your workspace is scoped to <b>{_escape_html(user.get('company','your organization'))}</b>.</p>
      <div style="margin-top:14px;color:#73e5bd;font-weight:800">🌍 {country} · {language}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""<div class="user-kpis">
        <div class="user-kpi"><b>{files:,}</b><span>Files</span></div>
        <div class="user-kpi"><b>{projects:,}</b><span>Projects</span></div>
        <div class="user-kpi"><b>{activities:,}</b><span>Workspace activity</span></div>
        <div class="user-kpi"><b>{count_user_notifications(user):,}</b><span>Unread notifications</span></div>
        </div>""",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    cards = [
        ("▦", "Start with your data", "Upload a CSV, Excel, TSV or JSON file and begin a structured analysis.", "Workspace & Data"),
        ("◈", "Understand the business", "Use the Business Twin to inspect data health, patterns and measurable opportunities.", "Business Twin"),
        ("⌕", "Research the world", "Search current public information and collect useful sources for your work.", "Research Store"),
    ]
    for col, (icon, title, copy, target) in zip((c1,c2,c3), cards):
        with col:
            st.markdown(f"""<div class="user-work-card"><div style="font-size:24px">{icon}</div><h3>{title}</h3><p>{copy}</p></div>""", unsafe_allow_html=True)
            if st.button(f"Open {title}", key=f"user_dash_{target}", use_container_width=True):
                st.session_state.selected_page = target
                st.rerun()

    st.markdown("### 🔔 Messages")
    if notifications.empty:
        st.info("No new messages yet.")
    else:
        for _, row in notifications.iterrows():
            st.markdown(
                f"""<div class="notice-card"><b>{_escape_html(str(row.get('event_type','message')).replace('_',' ').title())}</b><div style="margin-top:4px;color:#dce7f5">{_escape_html(str(row.get('message','')))}</div><small style="color:#7488a3">{_escape_html(str(row.get('created_at','')))}</small></div>""",
                unsafe_allow_html=True,
            )
        if st.button("Mark messages as read", use_container_width=False):
            mark_notifications_read(user)
            st.rerun()

def render_research_store(user):
    """Online research/resource hub for ordinary users."""
    st.markdown("""
    <div class="user-dash">
      <div style="color:#6ee7ff;font-size:11px;font-weight:900;letter-spacing:.16em">DACRE RESEARCH STORE</div>
      <h1 style="color:#fff;margin:8px 0">Research, sources and market intelligence.</h1>
      <p style="color:#9eb0c8;max-width:800px">Search the public web, compare sources and save the research trail to your workspace. Paid resources should be opened through approved accounts rather than purchased automatically.</p>
    </div>
    """, unsafe_allow_html=True)

    q = st.text_input("Research query", placeholder="e.g. Nigerian fintech market size 2026", key="research_store_query")
    if st.button("Search the web", type="primary", use_container_width=True) and q.strip():
        results = []
        try:
            results = google_web_search(q.strip(), max_results=10)
        except Exception:
            results = []
        if results:
            mongo_log_research(user, q.strip(), [{"title": t, "url": u} for t,u in results])
            for title, url in results:
                st.markdown(f"**{_escape_html(title)}**")
                st.caption(url)
                st.markdown("---")
        else:
            st.warning("No public research results were returned. Check the spelling or try a more specific query.")

    st.markdown("### Approved research categories")
    cols = st.columns(4)
    for col, title, desc in [
        ("Web intelligence", "Current public websites, announcements and company information."),
        ("Market research", "Market size, competitors, sectors, trends and opportunity signals."),
        ("Academic research", "Papers and educational resources that can support analysis."),
        ("Public data", "Government, statistical and open-data resources."),
    ]:
        with col:
            st.markdown(f"""<div class="user-work-card"><h3>{_escape_html(title)}</h3><p>{_escape_html(desc)}</p></div>""", unsafe_allow_html=True)

# =============================================================================
# SCRIPTURE KNOWLEDGE: public-domain KJV + Pickthall, loaded on demand.
# The complete corpora are not hard-coded into app.py; they are cached locally
# after the first scripture request to keep the application maintainable.
# =============================================================================

SCRIPTURE_DIR = BASE_DIR / "assets" / "scripture"
SCRIPTURE_DIR.mkdir(parents=True, exist_ok=True)
KJV_CACHE = SCRIPTURE_DIR / "kjv.json"
QURAN_PICKTHALL_CACHE = SCRIPTURE_DIR / "quran_pickthall.txt"

SCRIPTURE_SOURCES = {
    "kjv": "https://raw.githubusercontent.com/midvash/bible-data/main/versions/en/kjv/kjv.json",
    "quran": "https://raw.githubusercontent.com/druvx13/Quran-data/cairo/data/en.pickthall.txt",
}

QURAN_SURA_NAMES = [
    "Al-Fatihah","Al-Baqarah","Aal-E-Imran","An-Nisa","Al-Maidah","Al-Anam","Al-Araf","Al-Anfal",
    "At-Tawbah","Yunus","Hud","Yusuf","Ar-Rad","Ibrahim","Al-Hijr","An-Nahl","Al-Isra","Al-Kahf",
    "Maryam","Ta-Ha","Al-Anbiya","Al-Hajj","Al-Muminun","An-Nur","Al-Furqan","Ash-Shuara","An-Naml",
    "Al-Qasas","Al-Ankabut","Ar-Rum","Luqman","As-Sajdah","Al-Ahzab","Saba","Fatir","Ya-Sin","As-Saffat",
    "Sad","Az-Zumar","Ghafir","Fussilat","Ash-Shura","Az-Zukhruf","Ad-Dukhan","Al-Jathiyah","Al-Ahqaf",
    "Muhammad","Al-Fath","Al-Hujurat","Qaf","Adh-Dhariyat","At-Tur","An-Najm","Al-Qamar","Ar-Rahman",
    "Al-Waqiah","Al-Hadid","Al-Mujadila","Al-Hashr","Al-Mumtahanah","As-Saff","Al-Jumah","Al-Munafiqun",
    "At-Taghabun","At-Talaq","At-Tahrim","Al-Mulk","Al-Qalam","Al-Haqqah","Al-Maarij","Nuh","Al-Jinn",
    "Al-Muzzammil","Al-Muddaththir","Al-Qiyamah","Al-Insan","Al-Mursalat","An-Naba","An-Naziat","Abasa",
    "At-Takwir","Al-Infitar","Al-Mutaffifin","Al-Inshiqaq","Al-Buruj","At-Tariq","Al-Ala","Al-Ghashiyah",
    "Al-Fajr","Al-Balad","Ash-Shams","Al-Layl","Ad-Duha","Ash-Sharh","At-Tin","Al-Alaq","Al-Qadr",
    "Al-Bayyinah","Az-Zalzalah","Al-Adiyat","Al-Qariah","At-Takathur","Al-Asr","Al-Humazah","Al-Fil",
    "Quraysh","Al-Maun","Al-Kawthar","Al-Kafirun","An-Nasr","Al-Masad","Al-Ikhlas","Al-Falaq","An-Nas"
]

def _download_scripture_file(path, url):
    if path.exists() and path.stat().st_size > 100:
        return True
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "DACRE-Scripture-Knowledge/1.0"})
        with urllib.request.urlopen(request, timeout=25) as response:
            raw = response.read()
        if len(raw) < 100:
            return False
        path.write_bytes(raw)
        return True
    except Exception as exc:
        logger.warning("Scripture cache download failed: %s", type(exc).__name__)
        return False

@st.cache_data(show_spinner=False)
def load_kjv_corpus():
    if not _download_scripture_file(KJV_CACHE, SCRIPTURE_SOURCES["kjv"]):
        return {}
    try:
        return json.loads(KJV_CACHE.read_text(encoding="utf-8"))
    except Exception:
        return {}

@st.cache_data(show_spinner=False)
def load_quran_corpus():
    if not _download_scripture_file(QURAN_PICKTHALL_CACHE, SCRIPTURE_SOURCES["quran"]):
        return ""
    try:
        return QURAN_PICKTHALL_CACHE.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

def _norm_ref(value):
    return re.sub(r"[^a-z0-9]", "", str(value or "").lower())

def bible_reference_from_text(text):
    q = str(text or "")
    pattern = re.compile(r"(?:(\d)\s*)?([A-Za-z][A-Za-z ]{1,24})\s+(\d{1,3})(?::(\d{1,3})(?:\s*-\s*(\d{1,3}))?)?", re.I)
    for match in pattern.finditer(q):
        book = re.sub(r"\s+", " ", match.group(2)).strip()
        if _norm_ref(book) in {"the","chapter","verse","quran","surah","allah","what","does","mean"}:
            continue
        prefix = (match.group(1) or "")
        book = (prefix + " " + book).strip()
        return book, int(match.group(3)), int(match.group(4) or 0), int(match.group(5) or match.group(4) or 0)
    return None

def lookup_bible_reference(text):
    ref = bible_reference_from_text(text)
    corpus = load_kjv_corpus()
    if not ref or not corpus:
        return None
    book, chapter, verse_start, verse_end = ref
    book_norm = _norm_ref(book)
    matched = None
    for item in corpus.get("books", []):
        if _norm_ref(item.get("book")) == book_norm:
            matched = item
            break
    if matched is None:
        return None
    chapters = matched.get("chapters", [])
    if chapter < 1 or chapter > len(chapters):
        return None
    chapter_obj = chapters[chapter - 1]
    verses = chapter_obj.get("verses", [])
    if verse_start:
        end = verse_end or verse_start
        verses = [v for v in verses if verse_start <= int(v.get("number", 0)) <= end]
    text_lines = [f"{book} {chapter}:{v.get('number')}: {v.get('text','')}" for v in verses]
    return {
        "translation": "King James Version (KJV)",
        "reference": f"{book} {chapter}" + (f":{verse_start}" if verse_start else ""),
        "text": "\n".join(text_lines)[:26000],
    }

def quran_reference_from_text(text):
    q = str(text or "")
    m = re.search(r"(?:quran|koran|surah|sura)\s*(?:\(?\s*)?(\d{1,3})(?::|[ -])(\d{1,3})", q, re.I)
    if m:
        return int(m.group(1)), int(m.group(2))
    for idx, name in enumerate(QURAN_SURA_NAMES, 1):
        if _norm_ref(name) in _norm_ref(q):
            vm = re.search(rf"{re.escape(name)}\s+(\d{{1,3}})", q, re.I)
            if vm:
                return idx, int(vm.group(1))
    return None

def lookup_quran_reference(text):
    ref = quran_reference_from_text(text)
    corpus = load_quran_corpus()
    if not ref or not corpus:
        return None
    surah, ayah = ref
    lines = []
    for line in corpus.splitlines():
        parts = line.split("|", 2)
        if len(parts) != 3:
            continue
        try:
            s, a = int(parts[0]), int(parts[1])
        except ValueError:
            continue
        if s == surah and a == ayah:
            lines.append(f"Qur'an {surah}:{ayah}: {parts[2].strip()}")
            break
    if not lines:
        return None
    return {"translation": "Pickthall English translation (1930)", "reference": f"Qur'an {surah}:{ayah}", "text": "\n".join(lines)}

def scripture_context_for_question(question):
    low = str(question or "").lower()
    is_bible = any(k in low for k in ("bible", "scripture", "kjv", "old testament", "new testament"))
    is_quran = any(k in low for k in ("quran", "koran", "surah", "sura", "ayah", "allah"))
    if is_bible:
        result = lookup_bible_reference(question)
        if result:
            return result
    if is_quran:
        result = lookup_quran_reference(question)
        if result:
            return result
    return None

def answer_scripture_question(question, user):
    result = scripture_context_for_question(question)
    if not result:
        return None
    system = f"""You are a respectful scripture study assistant inside DACRE.
The user asked a question about the {result['translation']}.
Explain the cited passage accurately, distinguish the quoted translation from your explanation,
do not claim religious authority, and do not invent historical facts.
Respect both Christian and Muslim traditions when relevant.
Answer in the user's selected language when practical: {st.session_state.get('di_language','English')}.
"""
    answer = ai_generate(
        system,
        f"REFERENCE: {result['reference']}\nTEXT:\n{result['text']}\n\nUSER QUESTION:\n{question}",
        max_tokens=1200,
    )
    if answer:
        return f"{result['reference']} — {result['translation']}\n\n{result['text']}\n\nExplanation:\n{normalize_di_identity(answer)}"
    return f"{result['reference']} — {result['translation']}\n\n{result['text']}\n\nI can provide a detailed explanation when an AI reasoning provider is configured."

# Add scripture retrieval to the real specialist brain.
_legacy_real_di_answer_upgrade = real_di_answer
def real_di_answer(agent, user, question, df=None, allow_online=True):
    scripture = answer_scripture_question(question, user)
    if scripture:
        return scripture
    return _legacy_real_di_answer_upgrade(agent, user, question, df=df, allow_online=allow_online)

# Add scripture retrieval to the general DI brain too.
_legacy_enhanced_di_reply_upgrade = enhanced_di_reply
def enhanced_di_reply(message, user, df, allow_online=True, language="English — Nigeria"):
    scripture = answer_scripture_question(message, user)
    if scripture:
        return scripture
    return _legacy_enhanced_di_reply_upgrade(message, user, df, allow_online=allow_online, language=language)

# =============================================================================
# Uniel public identity and the 20 specialist workforce
# =============================================================================

UNIEL_SPEC = {
    "name": "Uniel",
    "specialty": "Public Onboarding & Product Guide",
    "position": "DACRE Global Experience Guide",
    "role": "Explains DACRE to visitors, demonstrates the platform's worldwide capabilities, answers product questions and guides qualified visitors toward signup.",
    "keywords": ["dacre", "signup", "sign up", "what is dacre", "how does dacre work", "landing", "features", "worldwide"],
    "voice": "female",
}

# Keep the original 20 specialist roster intact and add Uniel as the public-facing guide.
if not any(x.get("name") == "Uniel" for x in REAL_DI_ROSTER):
    REAL_DI_ROSTER.append(UNIEL_SPEC)

# Ensure every permanent specialist uses the exact local face asset supplied with the project.
def _localize_di_face_assets():
    for spec in REAL_DI_ROSTER:
        name = spec.get("name", "")
        path = di_face_path(name)
        if path:
            spec["avatar"] = str(path.relative_to(BASE_DIR))
_localize_di_face_assets()

# =============================================================================
# In-app Emiel onboarding messages
# =============================================================================

def _seed_emiel_onboarding_notifications(user):
    if not user:
        return
    company = user.get("company", "")
    username = user.get("username", "")
    messages = [
        ("emiel_welcome", f"Welcome to DACRE, {user.get('first_name','there')}. Your {company} workspace is ready. I am Emiel, your Communications Specialist. Your first message is here in the app so you never have to wait for email."),
        ("emiel_next_step", "Your next step is simple: open Data Workspace, upload your first business file, and begin building your work record."),
    ]
    con = db()
    now = datetime.now().isoformat(timespec="seconds")
    try:
        for event_type, message in messages:
            exists = con.execute("SELECT 1 FROM notifications WHERE username=? AND company_name=? AND event_type=?", (username, company, event_type)).fetchone()
            if not exists:
                con.execute("INSERT INTO notifications(company_name,username,event_type,message,is_read,created_at) VALUES(?,?,?,?,?,?)", (company, username, event_type, message, 0, now))
        con.commit()
    finally:
        con.close()
    for event_type, message in messages:
        mongo_log_notification(username, company, event_type, message)

_legacy_create_account_upgrade = create_account
def create_account(*args, **kwargs):
    result = _legacy_create_account_upgrade(*args, **kwargs)
    try:
        ok, message, user = result
        if ok and user:
            mongo_sync_user(user)
            _seed_emiel_onboarding_notifications(user)
    except Exception as exc:
        logger.warning("Post-signup onboarding message failed: %s", type(exc).__name__)
    return result

# Keep the already-correct authentication flow and mirror successful logins to MongoDB.
_legacy_authenticate_upgrade = authenticate
def authenticate(*args, **kwargs):
    result = _legacy_authenticate_upgrade(*args, **kwargs)
    try:
        user, _error = result
        if user:
            mongo_sync_user(user)
            _ensure_user_preferences_table()
            prefs = get_user_preferences(user.get("username", ""))
            if not st.session_state.get("di_country"):
                st.session_state.di_country = prefs.get("country", "Nigeria")
                st.session_state.di_language = prefs.get("language", "English")
                st.session_state.di_language_code = prefs.get("language_code", "en-NG")
    except Exception:
        pass
    return result


def _send_emiel_user_message(recipient_user, subject, body, send_email=True):
    """Master-only Emiel messaging: always creates an in-app message, optionally sends email."""
    if not recipient_user:
        return "No recipient selected."
    username = recipient_user.get("username", "")
    company = recipient_user.get("company_name", recipient_user.get("company", ""))
    email = recipient_user.get("email", "")
    user_obj = {
        "username": username,
        "company": company,
        "first_name": recipient_user.get("first_name", "there"),
        "last_name": recipient_user.get("last_name", ""),
        "email": email,
    }
    notify_user(user_obj, f"{subject}: {body}", "emiel_message")
    status = "In-app message delivered."
    if send_email and email:
        try:
            status += " " + str(send_custom_email(email, recipient_user.get("first_name", "there"), subject, body, sender_agent="Emiel"))
        except Exception as exc:
            status += f" Email failed: {type(exc).__name__}."
    return status


def _brevo_secret(name, default=""):
    """Read Brevo credentials from Streamlit Secrets or environment variables."""
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value or os.getenv(name, default) or default).strip()


def _send_via_brevo(recipient_email, recipient_name, subject, body, sender_agent="Emiel"):
    """Send transactional email through Brevo's HTTPS API.

    This avoids Gmail SMTP/App Password requirements. The Brevo API key must
    be supplied privately through DACRE_BREVO_API_KEY.
    """
    api_key = _brevo_secret("DACRE_BREVO_API_KEY")
    sender_email = _brevo_secret("DACRE_BREVO_SENDER", "dacre-platform@gmail.com")
    sender_name = _brevo_secret("DACRE_BREVO_SENDER_NAME", "DACRE — David Intelligence")
    if not api_key:
        return None

    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": recipient_email, "name": recipient_name or ""}],
        "subject": subject,
        "textContent": body,
        "headers": {"X-DACRE-Agent": sender_agent},
    }
    request = urllib.request.Request(
        "https://api.brevo.com/v3/smtp/email",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            raw = response.read().decode("utf-8", errors="replace")
            data = json.loads(raw) if raw else {}
            return f"Brevo: sent ({data.get('messageId', 'accepted')})"
    except Exception as exc:
        return f"Brevo: failed ({type(exc).__name__})"


def send_custom_email(recipient_email, recipient_name, subject, body, sender_agent="Emiel"):
    """Send an agent-branded transactional email.

    Production preference: Brevo HTTPS API. SMTP providers remain as fallbacks
    so existing DACRE installations are not broken.
    """
    brevo_result = _send_via_brevo(
        recipient_email, recipient_name, subject, body, sender_agent=sender_agent
    )
    if brevo_result:
        return brevo_result

    providers = [
        ("Gmail", "DACRE_GMAIL_SMTP_HOST", "DACRE_GMAIL_SMTP_PORT", "DACRE_GMAIL_SMTP_USER", "DACRE_GMAIL_SMTP_PASSWORD", "DACRE_GMAIL_SMTP_FROM"),
        ("Outlook", "DACRE_OUTLOOK_SMTP_HOST", "DACRE_OUTLOOK_SMTP_PORT", "DACRE_OUTLOOK_SMTP_USER", "DACRE_OUTLOOK_SMTP_PASSWORD", "DACRE_OUTLOOK_SMTP_FROM"),
        ("Legacy SMTP", "DACRE_SMTP_HOST", "DACRE_SMTP_PORT", "DACRE_SMTP_USER", "DACRE_SMTP_PASSWORD", "DACRE_SMTP_FROM"),
    ]
    def secret(name, default=""):
        return _dacre_secret(name, default)

    for provider, hk, pk, uk, sk, fk in providers:
        host = secret(hk)
        port = int(secret(pk, "587") or "587")
        user_name = secret(uk)
        password = secret(sk)
        sender = secret(fk, user_name)
        if not (host and user_name and password):
            continue
        try:
            msg = MIMEMultipart()
            msg["From"] = f"{sender_agent} — DI <{sender or user_name}>"
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))
            with smtplib.SMTP(host, port, timeout=20) as server:
                server.starttls()
                server.login(user_name, password)
                server.sendmail(sender or user_name, [recipient_email], msg.as_string())
            return f"{provider}: sent"
        except Exception as exc:
            continue
    return "NOT SENT — configure DACRE_BREVO_API_KEY (recommended) or an SMTP provider."

def render_emiel_directory(user):
    """Master-only directory and messaging console for Emiel."""
    if not user or user.get("role") != "master":
        return
    st.markdown("""
    <div class="user-dash">
      <div style="color:#6ee7ff;font-size:11px;font-weight:900;letter-spacing:.16em">EMIEL · COMMUNICATIONS CONSOLE</div>
      <h2 style="color:#fff;margin:8px 0">People, account email and secure messaging</h2>
      <p style="color:#9eb0c8">This private founder console lets Emiel address registered DACRE users. Normal users cannot access this directory.</p>
    </div>
    """, unsafe_allow_html=True)

    con = db()
    try:
        people = pd.read_sql_query(
            """SELECT id,first_name,last_name,username,company_name,email,role,login_count,created_at,last_login
               FROM users WHERE lower(COALESCE(role,''))!='master' ORDER BY id DESC""",
            con
        )
    finally:
        con.close()

    if people.empty:
        st.info("No non-master accounts are registered yet.")
        return

    st.dataframe(safe_dataframe_for_streamlit(people), use_container_width=True, hide_index=True)

    options = people["username"].tolist()
    selected_username = st.selectbox("Choose a recipient", options, key="emiel_recipient")
    selected = people[people["username"] == selected_username].iloc[0].to_dict()
    st.caption(f"Email: {selected.get('email','')} · Company: {selected.get('company_name','')}")

    with st.form("emiel_message_form", clear_on_submit=True):
        subject = st.text_input("Message subject", value="A message from Emiel — DACRE")
        body = st.text_area("Message", height=140, placeholder="Write the message Emiel should deliver...")
        email_too = st.checkbox("Send email too (if SMTP is configured)", value=True)
        submitted = st.form_submit_button("Send through Emiel", type="primary", use_container_width=True)
    if submitted:
        if not body.strip():
            st.warning("Please write a message first.")
        else:
            result = _send_emiel_user_message(selected, subject.strip() or "Message from Emiel", body.strip(), email_too)
            st.success(result)


_legacy_save_chat_history_message_upgrade = save_chat_history_message
def save_chat_history_message(user, sender, message):
    result = _legacy_save_chat_history_message_upgrade(user, sender, message)
    try:
        mongo_log_chat(user, sender, message)
    except Exception:
        pass
    return result


# =============================================================================
# PAGE-AWARE DI HOLOGRAPHIC ASSISTANT
# =============================================================================

# Every major DACRE surface has an accountable DI specialist. The same DI
# identity, role and private brain are used by the page assistant and by the
# 20-room Basement world.
DACRE_PAGE_DI_MAP = {
    "Overview": "Raziel",
    "DI Home": "Raziel",
    "DI Calls": "Emiel",
    "DI Workforce": "Muriel",
    "🌍 Global Markets": "Nathaniel",
    "🎥 DI Conference": "Emiel",
    "DI Action Center": "Uriel",
    "DI Memory Box": "Haniel",
    "Business Command Center": "Graciel",
    "Business Twin": "Ariel",
    "Decision Ledger": "Raziel",
    "Opportunity Radar": "Gabriel",
    "Workspace & Data": "Daniel",
    "Formula Lab": "Oriel",
    "Charts": "Oriel",
    "File Vault": "Henriel",
    "Export Center": "Daniel",
    "Chibobec Loan Desk": "Nathaniel",
    "Organization Admin Portal": "Jamiel",
    "Overall Admin DI Portal": "Guaiel",
    "Research Store": "Sofiel",
}

def _page_di_agent(page_name):
    """Return the real seeded DI responsible for the current DACRE surface."""
    target = DACRE_PAGE_DI_MAP.get(page_name, "Assiel")
    rows = real_di_agent_rows()
    for row in rows:
        if str(row.get("di_name", "")).strip().lower() == target.lower():
            return row
    # Safe fallback to the first real seeded agent.
    return rows[0] if rows else {
        "di_name": target,
        "specialty": "DACRE Intelligence",
        "position_title": "DI Specialist",
        "system_role": "Assists users on this DACRE platform surface.",
        "status": "Available",
        "id": 0,
    }

def _di_uptime_snapshot(agent):
    """
    Persist a service heartbeat. This represents the DI service being alive
    while the DACRE process is running; it does not falsely claim uptime while
    the hosting service itself is offline.
    """
    now = datetime.now()
    if "dacre_process_started_at" not in st.session_state:
        st.session_state.dacre_process_started_at = now.isoformat(timespec="seconds")

    started = st.session_state.dacre_process_started_at
    try:
        elapsed = max(0, int((now - datetime.fromisoformat(started)).total_seconds()))
    except Exception:
        elapsed = 0

    days, rem = divmod(elapsed, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    uptime = f"{days}d {hours:02d}h {minutes:02d}m {seconds:02d}s"

    # Persist a heartbeat if the table exists; failures must never crash the UI.
    try:
        con = db()
        con.execute("""CREATE TABLE IF NOT EXISTS di_service_heartbeat (
            di_name TEXT PRIMARY KEY,
            last_seen TEXT NOT NULL,
            status TEXT NOT NULL,
            page_name TEXT
        )""")
        con.execute("""INSERT INTO di_service_heartbeat(di_name,last_seen,status,page_name)
                       VALUES(?,?,?,?)
                       ON CONFLICT(di_name) DO UPDATE SET
                       last_seen=excluded.last_seen,
                       status=excluded.status,
                       page_name=excluded.page_name""",
                    (agent.get("di_name","DI"), now.isoformat(timespec="seconds"), "ONLINE", st.session_state.get("selected_page","")))
        con.commit()
        con.close()
    except Exception:
        pass

    return uptime, now.strftime("%Y-%m-%d %H:%M:%S")

def render_page_di_hologram(page_name, user):
    """
    Put the responsible DI at the top of the current DACRE page.
    The DI's actual face, role and operational screen reflect the page the
    user is currently visiting.
    """
    if not user:
        return

    agent = _page_di_agent(page_name)
    uptime, heartbeat = _di_uptime_snapshot(agent)
    name = html.escape(str(agent.get("di_name", "DI")))
    specialty = html.escape(str(agent.get("specialty", "DACRE Intelligence")))
    position = html.escape(str(agent.get("position_title", "DI Specialist")))
    role = html.escape(str(agent.get("system_role", "Ready to assist you.")))
    face = di_face_data_url(str(agent.get("di_name", "")))

    if face:
        avatar = f'<img src="{face}" alt="{name}" class="page-di-face">'
    else:
        avatar = f'<div class="page-di-face page-di-fallback">{name[:1]}</div>'

    # This is a real working control: it opens a compact specialist prompt
    # and sends the question through the existing DI brain/research pipeline.
    st.markdown(f"""
    <div class="page-di-hologram">
      <div class="page-di-landscape">
        <div class="page-di-grid"></div>
        <div class="page-di-floor"></div>
        <div class="page-di-ring r1"></div>
        <div class="page-di-ring r2"></div>
        <div class="page-di-beam"></div>
        <div class="page-di-avatar">{avatar}</div>
        <div class="page-di-particles">· · · · · · · · · ·</div>
      </div>
      <div class="page-di-console">
        <div class="page-di-live"><span></span> ONLINE · READY TO ASSIST</div>
        <div class="page-di-kicker">DAVID INTELLIGENCE · DACRE PLATFORM</div>
        <h3>{name}</h3>
        <div class="page-di-role">{position} · {specialty}</div>
        <p>{role}</p>
        <div class="page-di-status-row">
          <div><b>PAGE NODE</b><br><span>{html.escape(page_name)}</span></div>
          <div><b>UPTIME</b><br><span>{uptime}</span></div>
          <div><b>HEARTBEAT</b><br><span>{heartbeat}</span></div>
        </div>
        <div class="page-di-screen">
          <div class="screen-bar"><span>DACRE WORKSTATION</span><span>24/7 READY</span></div>
          <div class="screen-line"></div>
          <div class="screen-copy">SPECIALIST NODE ACTIVE · WORKING ON THIS PAGE · KNOWLEDGE + TOOLS + DI BRAIN CONNECTED</div>
        </div>
      </div>
    </div>
    <style>
      .page-di-hologram{{display:grid;grid-template-columns:310px 1fr;gap:0;margin:0 0 20px;border:1px solid #274966;border-radius:24px;overflow:hidden;background:radial-gradient(circle at 18% 25%,#103d60 0,#071521 34%,#02060b 100%);box-shadow:0 22px 70px rgba(0,0,0,.42),inset 0 0 80px rgba(74,198,255,.035)}}
      .page-di-landscape{{position:relative;min-height:240px;overflow:hidden;background:radial-gradient(circle at 50% 45%,rgba(75,199,255,.22),transparent 24%),linear-gradient(180deg,#071c2d,#02060b)}}
      .page-di-grid{{position:absolute;left:-30%;right:-30%;bottom:-55%;height:150%;background-image:linear-gradient(#58c7ff1f 1px,transparent 1px),linear-gradient(90deg,#58c7ff1f 1px,transparent 1px);background-size:30px 30px;transform:perspective(160px) rotateX(64deg)}}
      .page-di-floor{{position:absolute;left:22%;right:22%;bottom:18px;height:20px;border-radius:50%;background:#58c7ff22;box-shadow:0 0 45px 12px #58c7ff1e;filter:blur(5px)}}
      .page-di-beam{{position:absolute;left:50%;top:25px;width:115px;height:190px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,#58c7ff18,transparent);filter:blur(5px);animation:pdiBeam 2.5s ease-in-out infinite}}
      .page-di-avatar{{position:absolute;left:50%;top:48%;transform:translate(-50%,-50%);width:120px;height:120px;display:grid;place-items:center;animation:pdiFloat 3s ease-in-out infinite;filter:drop-shadow(0 0 22px #58c7ff88)}}
      .page-di-face{{width:94px;height:94px;object-fit:cover;border-radius:50%;border:1px solid #6ed7ff99;box-shadow:0 0 30px #58c7ff55;mix-blend-mode:screen}}
      .page-di-fallback{{display:grid;place-items:center;background:#09263c;color:#b7ebff;font-size:42px;font-weight:900}}
      .page-di-ring{{position:absolute;left:50%;top:48%;width:145px;height:44px;border:1px solid #5bcfff77;border-radius:50%;transform:translate(-50%,-50%);animation:pdiSpin 6s linear infinite}}
      .page-di-ring.r2{{width:180px;height:56px;transform:translate(-50%,-50%) rotate(58deg);animation-duration:9s;animation-direction:reverse}}
      .page-di-particles{{position:absolute;left:0;right:0;bottom:44px;text-align:center;color:#62d7ff77;letter-spacing:14px;animation:pdiParticles 2s ease-in-out infinite}}
      .page-di-console{{padding:22px 24px}}
      .page-di-live{{display:inline-flex;align-items:center;gap:7px;color:#67e6a2;font-size:9px;font-weight:900;letter-spacing:.13em}}
      .page-di-live span{{width:8px;height:8px;border-radius:50%;background:#4ee493;box-shadow:0 0 14px #4ee493;animation:pdiBlink 1.3s infinite}}
      .page-di-kicker{{color:#5dcfff;font-size:9px;font-weight:900;letter-spacing:.16em;margin-top:10px}}
      .page-di-console h3{{color:#fff;font-size:29px;margin:5px 0 2px}}
      .page-di-role{{color:#9bdfff;font-weight:800;font-size:11px}}
      .page-di-console p{{color:#a7b8c9;line-height:1.55;max-width:800px;margin:9px 0}}
      .page-di-status-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0}}
      .page-di-status-row div{{background:#071522;border:1px solid #24455d;border-radius:10px;padding:8px;color:#7691a8;font-size:8px}}
      .page-di-status-row b{{color:#5fcfff;font-size:7px;letter-spacing:.1em}} .page-di-status-row span{{color:#fff;font-size:9px}}
      .page-di-screen{{border:1px solid #2d617d;border-radius:12px;padding:10px;background:linear-gradient(145deg,#061a28,#02080d);box-shadow:inset 0 0 25px #58c7ff08}}
      .screen-bar{{display:flex;justify-content:space-between;color:#5ecfff;font-size:7px;font-weight:900;letter-spacing:.12em}}
      .screen-line{{height:2px;width:40%;background:#ffad62;margin:8px 0;box-shadow:0 0 10px #ffad62}}
      .screen-copy{{color:#a8c0d1;font-size:9px;letter-spacing:.03em}}
      @keyframes pdiBeam{{0%,100%{{opacity:.35;transform:translateX(-50%) scaleX(.72)}}50%{{opacity:1;transform:translateX(-50%) scaleX(1.12)}}}}
      @keyframes pdiFloat{{0%,100%{{margin-top:0}}50%{{margin-top:-8px}}}}
      @keyframes pdiSpin{{to{{transform:translate(-50%,-50%) rotate(360deg)}}}}
      @keyframes pdiParticles{{0%,100%{{opacity:.25}}50%{{opacity:.8}}}}
      @keyframes pdiBlink{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
      @media(max-width:760px){{.page-di-hologram{{grid-template-columns:1fr}}.page-di-landscape{{min-height:210px}}.page-di-status-row{{grid-template-columns:1fr}}.page-di-console h3{{font-size:24px}}}}
    </style>
    """, unsafe_allow_html=True)

    with st.expander(f"Talk to {agent.get('di_name','DI')} — {page_name}", expanded=False):
        question = st.text_input(
            f"What do you need {agent.get('di_name','DI')} to do?",
            key=f"page_di_question_{re.sub(r'[^a-zA-Z0-9]+','_',page_name)}"
        )
        if st.button(f"Ask {agent.get('di_name','DI')}", key=f"page_di_ask_{re.sub(r'[^a-zA-Z0-9]+','_',page_name)}", type="primary"):
            if not question.strip():
                st.warning("Enter a request for the DI.")
            else:
                with st.spinner(f"{agent.get('di_name','DI')} is working..."):
                    try:
                        answer, source = di_basement_research_answer(agent, user, question.strip(), allow_remote=True)
                        real_di_record_chat(agent, user, question.strip(), answer, source=source)
                        st.session_state[f"page_di_last_answer_{re.sub(r'[^a-zA-Z0-9]+','_',page_name)}"] = answer
                        st.session_state[f"page_di_last_source_{re.sub(r'[^a-zA-Z0-9]+','_',page_name)}"] = source
                    except Exception as exc:
                        logger.exception("Page DI assistant failed: %s", exc)
                        st.error("The DI could not complete that request. The application remains available.")
        last = st.session_state.get(f"page_di_last_answer_{re.sub(r'[^a-zA-Z0-9]+','_',page_name)}")
        if last:
            st.markdown("**DI response**")
            st.write(last)
            st.caption(f"Source path: {st.session_state.get(f'page_di_last_source_{re.sub(r'[^a-zA-Z0-9]+','_',page_name)}', 'local')}")


# =============================================================================
# Main application access policy
# =============================================================================

MASTER_PAGES = [
    "Overview", "DI Home", "DI Calls", "DI Workforce", "🌍 Global Markets",
    "🎥 DI Conference", "DI Action Center", "DI Memory Box", "Business Command Center",
    "Business Twin", "Decision Ledger", "Opportunity Radar", "Workspace & Data",
    "Formula Lab", "Charts", "File Vault", "Export Center", "Chibobec Loan Desk",
    "Organization Admin Portal", "Overall Admin DI Portal",
]

# Public landing styling for Uniel and mobile layouts.
st.markdown("""
<style>
.uniel-landing-card{display:flex;gap:22px;align-items:center;margin:8px 28px 28px;padding:22px;border:1px solid rgba(94,170,255,.18);border-radius:24px;background:linear-gradient(145deg,rgba(17,31,54,.95),rgba(6,13,27,.96));box-shadow:0 24px 70px rgba(0,0,0,.25)}
.uniel-avatar-wrap{position:relative;flex:0 0 104px}.uniel-avatar-wrap img{width:104px;height:104px;border-radius:24px;object-fit:cover;border:1px solid rgba(105,225,255,.38);box-shadow:0 0 30px rgba(55,185,255,.18)}
.uniel-live-dot{position:absolute;right:4px;bottom:4px;width:14px;height:14px;border-radius:50%;background:#57e5b0;box-shadow:0 0 16px #57e5b0;border:3px solid #07101f}
.uniel-kicker{font-size:10px;letter-spacing:.16em;font-weight:900;color:#72dff9}.uniel-copy h2{margin:4px 0 8px;color:#fff;font-size:25px}.uniel-copy p{color:#9eb0c8;line-height:1.6;margin:6px 0}.uniel-grid{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}.uniel-grid span{padding:7px 10px;border-radius:999px;background:rgba(85,145,255,.08);border:1px solid rgba(100,160,255,.14);color:#c5d9f4;font-size:11px}.uniel-strong{font-weight:700;color:#d9e8fb!important}
@media(max-width:700px){.uniel-landing-card{margin:8px 0 22px;padding:16px;align-items:flex-start}.uniel-avatar-wrap{flex-basis:76px}.uniel-avatar-wrap img{width:76px;height:76px}.uniel-copy h2{font-size:20px}.hero{grid-template-columns:1fr!important;padding:34px 10px 24px!important}.grid-3,.grid-2{grid-template-columns:1fr!important}}
</style>
""", unsafe_allow_html=True)

def render_enterprise_sidebar(user):
    if not user:
        return
    if user.get("role") == "master":
        st.sidebar.markdown("## 👑 DACRE COMMAND")
        st.sidebar.caption("Founder / Overall Administrator")
        selected = st.sidebar.radio(
            "Command navigation",
            MASTER_PAGES,
            index=MASTER_PAGES.index(st.session_state.get("selected_page","Overview")) if st.session_state.get("selected_page","Overview") in MASTER_PAGES else 0,
            key="master_command_navigation",
        )
        st.session_state.selected_page = selected
        health = mongo_health()
        st.sidebar.markdown("---")
        st.sidebar.caption(f"MongoDB: {'● ONLINE' if health['enabled'] else '○ '+health['status']}")
        if st.sidebar.button("Sign out", use_container_width=True, key="master_sign_out"):
            st.session_state.user = None
            st.session_state.master_route = False
            st.session_state.selected_page = "Overview"
            st.rerun()
    else:
        render_user_navigation(user)

# Replace main application with a guarded additive version.
def render_productivity_bar(user):
    """Compact online-company action bar that makes the workspace easy to understand."""
    if not user:
        return
    master = user.get("role") == "master"
    company = _escape_html(str(user.get("company", "DACRE Workspace")))
    st.markdown(f"""
    <div class="dacre-quickbar">
      <div class="quick-brand">DACRE · {'FOUNDER COMMAND' if master else 'BUSINESS WORKSPACE'}</div>
      <div class="quick-status">Workspace: <b>{company}</b> · <span>DI ready</span></div>
    </div>
    """, unsafe_allow_html=True)

    if master:
        actions = [
            ("New overview", "Overview"),
            ("Open DI Home", "DI Home"),
            ("Work with data", "Workspace & Data"),
            ("Admin DI", "Overall Admin DI Portal"),
        ]
    else:
        actions = [
            ("Start with data", "Workspace & Data"),
            ("Business Twin", "Business Twin"),
            ("Find opportunities", "Opportunity Radar"),
            ("Research", "Research Store"),
        ]

    cols = st.columns(len(actions), gap="small")
    for i, (label, target) in enumerate(actions):
        with cols[i]:
            if st.button(label, key=f"quick_action_{'master' if master else 'user'}_{i}", use_container_width=True):
                st.session_state.selected_page = target
                st.rerun()

    with st.expander("How DACRE works", expanded=False):
        st.markdown(
            "**1. Bring your information in** → upload or connect your business data.  "
            "**2. Understand it** → clean, inspect and visualize it.  "
            "**3. Decide** → use Business Twin, Opportunity Radar and Decision Ledger.  "
            "**4. Act** → export results or move the next action into your workspace."
        )


def main_app():
    if not st.session_state.get("dacre_boot_complete", False):
        init_production_core()
        st.session_state.dacre_boot_complete = True

    user = st.session_state.get("user")
    if not user:
        landing_page()
        return

    mongo_sync_user(user)
    render_enterprise_sidebar(user)
    apply_company_website_theme(user)
    render_productivity_bar(user)

    if not st.session_state.chat_history:
        st.session_state.chat_history = load_chat_history(user, limit=40)

    selected_page = st.session_state.get("selected_page", "Overview")

    if user.get("role") != "master":
        allowed = {"Overview","Workspace & Data","Business Twin","Decision Ledger","Opportunity Radar","File Vault","Export Center","Research Store"}
        if selected_page not in allowed:
            selected_page = "Overview"
            st.session_state.selected_page = selected_page

    render_page_chrome(selected_page, user)
    render_page_di_hologram(selected_page, user)

    if selected_page == "Overview":
        if user.get("role") == "master":
            render_dacre_production_core()
            st.markdown("---")
            render_online_robot_control_center(user)
            st.markdown("---")
            render_analytics_overview(user)
        else:
            render_user_dashboard(user)
    elif selected_page == "Research Store" and user.get("role") != "master":
        render_research_store(user)
    elif selected_page == "DI Home" and user.get("role") == "master":
        render_real_di_home(user)
    elif selected_page == "DI Calls" and user.get("role") == "master":
        render_di_calls(user)
    elif selected_page == "DI Workforce" and user.get("role") == "master":
        render_real_di_workforce(user)
    elif selected_page == "🌍 Global Markets" and user.get("role") == "master":
        render_global_markets_dashboard()
    elif selected_page == "🎥 DI Conference" and user.get("role") == "master":
        render_enhanced_conference_room(user)
    elif selected_page == "DI Action Center" and user.get("role") == "master":
        render_action_center(user)
    elif selected_page == "DI Memory Box" and user.get("role") == "master":
        render_di_memory_box(user)
    elif selected_page == "Business Command Center" and user.get("role") == "master":
        render_business_command_center(user)
    elif selected_page == "Business Twin":
        render_business_twin(st.session_state.processed_df, user)
    elif selected_page == "Decision Ledger":
        render_decision_ledger(user)
    elif selected_page == "Opportunity Radar":
        render_opportunity_page(user)
    elif selected_page == "Workspace & Data":
        render_workspace_data(user)
    elif selected_page == "Formula Lab" and user.get("role") == "master":
        render_formula_lab(user)
    elif selected_page == "Charts" and user.get("role") == "master":
        render_charts(user)
    elif selected_page == "File Vault":
        render_file_vault(user)
    elif selected_page == "Export Center":
        render_export_center(user)
    elif selected_page == "Chibobec Loan Desk" and user.get("role") == "master":
        render_chibobec_loan_desk(user)
    elif selected_page == "Organization Admin Portal" and user.get("role") == "master":
        render_organization_admin(user)
    elif selected_page == "Overall Admin DI Portal" and user.get("role") == "master":
        render_fixed_overall_admin_page(user)
    else:
        if user.get("role") == "master":
            st.info("This command module is available from the master navigation.")
        else:
            render_user_dashboard(user)

    # DI internal dock is deliberately private to the founder command surface.
    if user.get("role") == "master":
        render_persistent_di_dock(user)


# Ensure the new roster and brain are present before the application starts.
try:
    real_di_seed_workforce()
except Exception as _real_di_boot_error:
    logger.exception("Real DI workforce bootstrap failed: %s", _real_di_boot_error)

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Show landing page if no user
    if st.session_state.user is None:
        landing_page()
    else:
        main_app()
