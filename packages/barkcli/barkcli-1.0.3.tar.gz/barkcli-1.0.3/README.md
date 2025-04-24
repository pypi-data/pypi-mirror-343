
# barkcli

一个基于 [BarkNotificator](https://github.com/funny-cat-happy/barknotificator) 的命令行工具，支持通过命令行发送推送通知到 Bark 应用。

## 安装

从[realese页下载](https://github.com/falconchen/barkcli/releases/)：

```bash
pip install barkcli-.*.tar.gz
```

或从源码目录运行：

```bash
pip install .
```

## 使用方法

### 设置 Token

你可以通过环境变量 `BARK_TOKEN` 设置设备 token：

```bash
export BARK_TOKEN=your_device_token
```

也可以通过 `--token` 参数传入。

### 命令格式

支持位置参数和具名参数：

#### 位置参数（按顺序）

```bash
bark "Title" "Message content" "https://icon.url" "https://target.url" "category" "alarm.caf"
```

#### 具名参数

```bash
bark --title "Hello" --content "World" \
     --icon_url "https://..." \
     --target_url "https://..." \
     --category "group1" \
     --ringtone "alarm.caf"
```

## 参数说明

- `title`: 推送标题
- `content`: 推送内容
- `icon_url`: 图标 URL
- `target_url`: 点击跳转 URL
- `category`: Bark 分类（用于分组显示）
- `ringtone`: 铃声名称（如：`alarm.caf`, `bell.caf`）

## 打包成压缩文件
在修正后的 barkcli 项目目录下执行：
```
python setup.py sdist
```
会在 `dist/` 目录生成一个新的 `barkcli-x.x.x.tar.gz` 文件

## 重新安装到系统
pip install --force-reinstall dist/barkcli-*.tar.gz
