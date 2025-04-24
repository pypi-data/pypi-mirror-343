# Esewa Profanity Detection Package

This package is mainly used for detecting profanity for different languages specially, with Devnagari and Latin script.

Overall package is structured in the following way:

```
Esewa-Profanity-Detection
|--- key_generator: Generates key for encrypting files.
|---encryptor : Encrypts the plain text file to encrypted files.
|---files : Directory for storing key, encrypted files and unicode files.
|---profanity_detector: Library for detecting profanity.
```

## 1. Key generator

Key generator uses Fernet and generates key. The generated key is stored in `files > keys`.

Basically one key is generated and overriden. i.e. `secret.key`.

But the immutable key `static_secret.key` is always placed.

Use the class `KeyGenerator` to instantiate and run method `generate()` from the package to generate unique secret key.

### Importing `KeyGenerator` class and using it.
```Python
>> from esewa_profanity import KeyGenerator

>> key_generator = KeyGenerator()
>> key_generator.generate()
```

User Program Location for windows : `C:\Users\<Username>\AppData\Local\Programs`
### Output:

>> Secret Key generated in the location: `<User-program-location>\Python\Python313\Lib\site-packages\esewa_profanity\files\keys\secret.key`

## 2. Encryptor

Encryptor enccrypts the plain text file given by the User and stores the data into `files > encoded_files`.

Two keys (`secret.key` and `static_secret.key`)are used for encrypting files. 

`static_secret.key` encrypts the predefined english and nepali bad words file.

`secret.key` encrypts the custom english and nepali bad words file.

Encrypted files will be in `.enc` format files.

Use the class `PreDefinedEncryptor` to instantiate and run method `encrypt(english_file, nepali_file)` in order to encrypt predefined english and nepali file. 

![Custom encryptor](/src/custom_encryption.png)

Use the class `CustomEncryptor` to instantiate and run method `encrypt(is_itreable=True, english_itreable, nepali_itreable)` in order to encrypt custom english and nepali list or set.

Use the class `CustomEncryptor` to instantiate and run method `encrypt(is_itreable=False, english_file, nepali_file)` in order to encrypt custom english and nepali file.


### Importing `PreDefinedEncrytor` class and using it.
```Python
>> from esewa_profanity import PreDefinedEncryptor
>> encryptor = PreDefinedEncryptor()
>> encryptor.encrypt('<Location of .txt english file>', '<Location of .txt nepali romanized file>')

```


### Output for `PredefinedEncryptor` class:

>> Encrypted bad words saved to : ```<User-program-location>\Python\Python313\Lib\site-packages\esewa_profanity\files\encoded_files\english_badwords.enc```

>> Encrypted bad words saved to :
``` <User-program-location>\Python\Python313\Lib\site-packages\esewa_profanity\files\encoded_files\nepali_badwords.enc```


### Importing `CustomEncryptor` class and encrypting file.
```Python
>> from esewa_profanity import CustomEncryptor
>> custom_encryptor = CustomEncryptor()
# Note that, is_itreable_passed must be False for the plain text file encryption.
>> custom_encryptor.encrypt(is_itreable_passed = False, 
english_plaintext_file = '<Location of .txt english file>', nepali_plaintext_file='<Location of .txt nepali romanized file>')
```


### Output for `CustomEncryptor` class after encrypting file:


>> Encrypted bad words saved to : ```<User-program-location>\Python\Python313\Lib\site-packages\esewa_profanity\files\encoded_files\custom_english_badwords.enc```

>> Encrypted bad words saved to : ```<User-program-location>\Python\Python313\Lib\site-packages\esewa_profanity\files\encoded_files\custom_nepali_badwords.enc```


### Importing `CustomEncryptor` class and encrypting itreables (Set or List).
```Python
>> from esewa_profanity import CustomEncryptor
>> custom_encryptor = CustomEncryptor()
# Note that, is_itreable_passed must be True for the english and nepali itreable files.
>> custom_encryptor.encrypt(is_itreable_passed = True, english_itreable = ['thong'], nepali_itreable=['Morr'])
```


### Output for `CustomEncryptor` class after encrypting file:


>> Encrypted bad words saved to : ```<User-program-location>\Python\Python313\Lib\site-packages\esewa_profanity\files\encoded_files\custom_english_badwords.enc```
>> Encrypted bad words saved to : ```<User-program-location>\Python\Python313\Lib\site-packages\esewa_profanity\files\encoded_files\custom_nepali_badwords.enc```


## 3. Profanity Detector

Profanity detector takes up text from the user. If the profanity is detected, then system provides user the prompt of profanity.

The encrypted file is now, decrypted with the key generated. For custom badwords, decryption is done with `secret.key` whereas for predefined badwords decryption is done with `static_secret.key`.


Use the class `ProfanityChecker` to instantiate and run method `detect_profanity(text)` with the `text` to detect profanity.

![Profanity Detection](/src/profanity_detection.png)

### Importing `ProfanityChecker` class and detecting text.
1. Example 1 (Profanity texts)

```Python
>> from esewa_profanity import ProfanityChecker
>> detector = ProfanityChecker()
>> detector.detect_profanity('Hello fvck Ganj* with thong, morr')
```

### Output:

>> Detected content is inappropriate/offensive. Kindly rephrase your message.

2. Example 2 (Non profanity Normal texts)

```Python
>> from esewa_profanity import ProfanityChecker
>> detector = ProfanityChecker()
>> detector.detect_profanity('Hello, I am ankit.')
```

### Output:

>> Your message is appropriate.