# 算子调试

安装 CANN Toolkit 9.0 或兼容版本、CMake，以及 Python 依赖：

```bash
source /path/to/cann/set_env.sh
python3 -m pip install -r requirements.txt
```

编辑 `kernel.asc` 后执行：

```bash
bash run.sh npu  # 需要昇腾设备；bash run.sh 默认也是此模式
bash run.sh cpu  # CPU 调测，无需昇腾设备
```

脚本依次编译、生成一个样例的输入和参考结果、运行、比较输出。
空实现通常报告 `Wrong Answer` 并返回退出码 1；输出正确返回 0，其他错误非零退出。
两种模式的产物分别保存在 `build-npu/` 和 `build-cpu/`。
CPU 模式使用 CANN 支持的 CPU 调测接口，不能用于测量 NPU 性能。

可选参数示例：

```bash
DEVICE_ID=1 BUILD_JOBS=4 PYTHON=python3 bash run.sh npu
NPU_ARCH=dav-2201 bash run.sh cpu
```

`reference.py` 如使用额外 Python 库，需要另行安装。
