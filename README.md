# VKGraph
Simple VK friends graph creator and viewer

## Requires
* VK API module
* flask server
## How to
1. Firstly you need to install VK API module and flask
``` bash
pip install vk_api flask
```

2. Set TOKEN in Creator/main.py (you can get token in [https://vk.com/dev](https://vk.com/dev))
3. Run Creator/main.py (it must be run from Creator folder, cause it uses relational pathes) and enter your VK ID, now it could be link to the page after `https://vk.com/`
4. After some time (you can drink your coffee or tea) your graph will be ready to view. It is in Viewer/users.json
5. Flask server will be started and you can go to web page to check your graph!
