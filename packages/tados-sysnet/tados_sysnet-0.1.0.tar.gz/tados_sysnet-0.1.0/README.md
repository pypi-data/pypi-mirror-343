Send files to other systems using Sysnet.

Example:
```py
import tados_sysnet as sn

username, password = "Kočička", "*******"

systemID = sn.login(username, password)
if not systemID:
    print("Invalid credentials!")
    exit(1)

for file in sn.getQueue(username, password):
    print(file)
```