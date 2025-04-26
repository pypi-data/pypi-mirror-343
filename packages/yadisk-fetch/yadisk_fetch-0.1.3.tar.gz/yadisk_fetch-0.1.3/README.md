# yadisk-fetch

Download public Yandex.Disk folders easily by faking a mobile browser and bypassing "install our app" popups.

## Why?

Yandex tries to force desktop users to install their app when downloading large folders.  
Mobile users, however, can download directly without installing anything.  
This tool pretends to be a mobile browser and lets you download files and folders directly.

## Installation

```
pip install yadisk-fetch
```

## Usage

```
yadisk-fetch <public_yandex_disk_link>
```

Example:

```
yadisk-fetch https://disk.yandex.ru/d/gWW6aj1qWDdfTg
```

The file will be downloaded and saved as `yadisk_download.zip` in the current directory.

## Notes

- Only works for public links.
- Large folders are automatically zipped by Yandex for mobile devices — this tool takes advantage of that.
- If Yandex triggers a CAPTCHA, you may need to manually solve it in a browser first.

## License

MIT License
