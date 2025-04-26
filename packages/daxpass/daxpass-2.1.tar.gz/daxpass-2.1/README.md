Dax let's you not only create passwords with custom requirements, it can also encode and decode strings in your own custom charset!

___

**DISCLAIMER**

It is recommended that dax should only be used in your own custom databases/servers, dax is not secure to use when creating passwords for products like Google. We are also not responsible for any harm according to the MIT license.
___

createpass:
```python
import daxpass

print(daxpass.createpass(['a', 'b'], 5))
```
Output:
baaba

___

en:
```python
import daxpass
print(daxpass.en('abc', ['a', 'b', 'c']))
```
Output:
```
- -- ---
```
___

de:
```python
import daxpass
print(daxpass.de('- -- ---', ['a', 'b', 'c']))
```
Output:
```
abc
```
