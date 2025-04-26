(ORIGINALLY KNOWN AS DAXPASS)

amuesm let's you not only create passwords with custom requirements, it can also encode and decode strings in your own custom charset! amuesm stand for:

- Annie's 
- Multi
- Use
- Encryption
- Security
- Module


___

**DISCLAIMER**

It is recommended that amuesm should only be used in your own custom databases/servers, amuesm is not secure to use when creating passwords for products like Google. We are also not responsible for any harm according to the MIT license.
___

createpass:
```python
import amuesm

print(amuesm.createpass(['a', 'b'], 5))
```
Output:
baaba

___

en:
```python
import amuesm

print(amuesm.en('abc', ['a', 'b', 'c']))
```
Output:
```
- -- ---
```
___

de:
```python
import amuesm

print(amuesm.de('- -- ---', ['a', 'b', 'c']))
```
Output:
```
abc
```
