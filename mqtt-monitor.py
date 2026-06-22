import time
import os
import re

# Percorso del file di log di Mosquitto (collegato al volume Docker)
LOG_FILE_PATH = "./mosquitto/log/mosquitto.log"

# Espressione regolare per intercettare i fallimenti di autenticazione di Mosquitto
# Esempio di log: "2026-06-22 18:00:00: Client <unknown> disconnected due to malformed packet." 
# Oppure: "2026-06-22 18:00:00: Socket error on client <unknown>, disconnecting."
AUTH_FAIL_PATTERN = re.re = re.compile(r"Connection refused: bad user name or password from ([0-9.]+)")

# Dizionario per tracciare i tentativi falliti per ogni IP
failed_attempts = {}
THRESHOLD = 3 # Limite di tentativi prima dell'allarme

def monitor_mosquitto_logs():
    print(f"[*] Starting MQTT Live Log Monitoring on: {LOG_FILE_PATH}")
    print("[*] Watching for Brute Force patterns...")

    # Se il file non esiste ancora, lo creiamo per evitare crash
    if not os.path.exists(LOG_FILE_PATH):
        os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
        with open(LOG_FILE_PATH, "w") as f:
            f.write("--- Mosquitto Log Monitor Started ---\n")

    with open(LOG_FILE_PATH, "r") as f:
        # Ci posizioniamo alla fine del file per leggere solo i nuovi log (tail -f)
        f.seek(0, os.SEEK_END)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1) # Aspetta nuove righe senza sovraccaricare la CPU
                continue
            
            # Analizza la riga di log
            match = AUTH_FAIL_PATTERN.search(line)
            if match:
                attacker_ip = match.group(1)
                failed_attempts[attacker_ip] = failed_attempts.get(attacker_ip, 0) + 1
                
                print(f"[!] Warning: Failed auth attempt from {attacker_ip} ({failed_attempts[attacker_ip]}/{THRESHOLD})")
                
                if failed_attempts[attacker_ip] >= THRESHOLD:
                    print(f"\n[🚨] CRITICAL ALARM: Brute Force detected from IP: {attacker_ip}!")
                    print(f"[🛡️] ACTION REQUIRED: Triggering IP ban/iptables rule for {attacker_ip}\n")
                    # Qui in produzione si inserisce la chiamata di sistema per bloccare l'IP
                    failed_attempts[attacker_ip] = 0 # Reset dopo l'allarme

if __name__ == "__main__":
    try:
        monitor_mosquitto_logs()
    except KeyboardInterrupt:
        print("\n[*] Monitoring stopped by user.")