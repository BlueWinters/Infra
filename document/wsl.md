
## WSL2

- 启用WSL和虚拟机功能（管理员权限）
 
```powershell
# 启用 WSL
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# 启用虚拟机平台（WSL2 所需）
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 执行完后需要 重启电脑 
```

- 设置 WSL2 为默认版本

```powershell
wsl --set-default-version 2
```

