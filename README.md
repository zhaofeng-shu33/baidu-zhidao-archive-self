Archive contents belonging to yourself in Baidu Zhidao

## How to
First you need to save the answer list in a file `list.html`,
change the encoding manually to `utf-8`.

The answer list can be downloaded using browser from the address
`https://zhidao.baidu.com/usercenter?uid=your_uid`. You should touch the bottom of the answer list to save the whole.

Then you need to create a directory `build` and run `python3 generate.py`.
The dependency is installed by `pip3 install --user -r requirements.txt`.
