bot.send_message(chat_id=CHAT_ID, text="🔔 这是一条测试消息，脚本启动正常！")
import requests
import time
import os
from telegram import Bot

# ================== 在这里填你的配置 ==================
TOKEN = "8841415360:AAFFAyhiRoZ2Q4y8UqE0lxMC8J6sQ_eAu48"   # ← 填你的真实完整 Token
CHAT_ID = 1804284015                                       # ← 你的 Chat ID

USDG_MINT = "2u1tszSeqZ3qBWF3uNGPFc8TzMk2tdiwknnRMWGWjGWH"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
AMOUNT = 10000 * 1000000            # 10000 USDG

# 你想设置的阈值（可自行修改）
THRESHOLD_LOW = 0.9999     # USDG 太便宜时提醒
THRESHOLD_HIGH = 1.0000    # USDG 太贵时提醒

CHECK_INTERVAL = 30       # 检查间隔（秒），建议 20-60 秒
# =====================================================

bot = Bot(token=TOKEN)

def get_jupiter_quote():
    url = "https://quote-api.jup.ag/v6/quote"
    params = {
        "inputMint": USDG_MINT,
        "outputMint": USDC_MINT,
        "amount": AMOUNT,
        "slippageBps": 50
    }
    data = requests.get(url, params=params).json()
    usdc_out = int(data.get('outAmount', 0)) / 1000000
    ratio = usdc_out / 10000
    return usdc_out, ratio

print("🚀 USDG → USDC 监控已启动...")

while True:
    try:
        usdc_out, ratio = get_jupiter_quote()
        
        if ratio < THRESHOLD_LOW or ratio > THRESHOLD_HIGH:
            message = f"""🚨 **USDG/USDC 比例异常警报！**

10000 USDG ≈ **{usdc_out:.2f}** USDC
当前比例: **{ratio:.4f}**

⚡ 建议立即前往 https://jup.ag 兑换"""
            
            bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
            print(f"✅ 已发送警报！比例: {ratio:.4f}")
        else:
            print(f"正常 | 比例: {ratio:.4f} | 可兑 {usdc_out:.2f} USDC")
            
    except Exception as e:
        print("请求出错:", e)
    
    time.sleep(CHECK_INTERVAL)
