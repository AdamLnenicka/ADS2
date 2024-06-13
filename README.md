# Zadání
Cílem projektu je vytvořit funkční aplikaci pro zpracování dat ze senzorů pro měření teploty.
Data budou produkována do Kafka clusteru běžícího v Kubernetes a z něj čtena aplikací
napsanou v libovolném programovacím jazyce, která poběží v Kubernetes také.
Projekt se nebude odevzdávat, ale bude se prezentovat osobně.
Požadavky:
1. Spusťte lokální Kubernetes cluster na svém (jednom) stroji.
2. Vytvořte v Kubernetes Kafka cluster se třemi brokery. Perzistenci dat v Kubernetes
řešit nemusíte. Nápověda pokud použijete Docker image Kafky od Bitnami: parametr
KAFKA_CFG_LISTENERS se vztahuje vždy k portům uvnitř kontejneru, takže i pokud
definujete nějaké EXTERNAL rozhraní Kafky, tak port v tomto parametru uveďte stejně
vnitřní.
3. Vytvořte v Kafka clusteru topic "temperature" se čtyřmi partition a třemi replikami.
4. Ověřte, že cluster funguje i při ztrátě (restart nebo dlouhodobé vypnutí) jednoho nebo
dvou brokerů.
5. Vytvořte v libovolném programovacím jazyce aplikaci “temperature_reader”, která:
a. Bude konzumovat zprávy z Kafka clusteru z topicu “temperature”. Použité
řešení musí zůstat funkční při výpadku libovolných brokerů Kafka clusteru.
b. Formát zprávy si můžete zvolit vlastní, ale musí obsahovat minimálně textový
identifikátor senzoru a také hodnotu naměřené teploty (ve °C, s přesností na
desetiny a v rozsahu vhodném pro běžnou domácnost - mimo tento rozsah
musí zprávy zahazovat).
c. Bude číst pouze nejnovější zprávy z Kafky.
d. Na výstupu bude vypisovat aplikace ke každé zprávě unikátní identifikátor
instance aplikace a za ním obsah načtené zprávy.
6. Zajistěte, aby aplikace temperature_reader běžela v Kubernetu ve dvou instancích.
7. Zajistěte, aby parametr “topic” pro temperature_reader byl konfigurovatelný
z Kubernetes.
8. Vyzkoušejte rolling update aplikace temperature_reader.

## Řešení
1. Spustit lokální Kubernetes cluster na svém (jednom) stroji.<br>

Pomocí minikube
```cmd
minikube start
```
2. Vytvořte v Kubernetes Kafka cluster se třemi brokery. Perzistenci dat v Kubernetes
řešit nemusíte. Nápověda pokud použijete Docker image Kafky od Bitnami: parametr
KAFKA_CFG_LISTENERS se vztahuje vždy k portům uvnitř kontejneru, takže i pokud
definujete nějaké EXTERNAL rozhraní Kafky, tak port v tomto parametru uveďte stejně
vnitřní.<br>

📂 [k8s/kafka.yaml](https://github.com/AdamLnenicka/ADS2/blob/main/k8s/kafka.yaml)<br>
📂 [k8s/zookeeper.yaml](https://github.com/AdamLnenicka/ADS2/blob/main/k8s/zookeeper.yaml)

```cmd
cd k8s/

kubectl apply -f .
```

3. Vytvořte v Kafka clusteru topic "temperature" se čtyřmi partition a třemi replikami.<br>
```cmd
kubectl exec -it kafka-0 -- bash
```
```cmd
kafka-topics.sh --bootstrap-server kafka:9092 --create --topic temperature --replication-factor 3 --partitions 4
```

4. Ověřte, že cluster funguje i při ztrátě (restart nebo dlouhodobé vypnutí) jednoho nebo
dvou brokerů.
```cmd
kubectl delete pod kafka-1
kubectl delete pod kafka-2
```
5. Vytvořte v libovolném programovacím jazyce aplikaci “temperature_reader”, která:<br>
a. Bude konzumovat zprávy z Kafka clusteru z topicu “temperature”. Použité
řešení musí zůstat funkční při výpadku libovolných brokerů Kafka clusteru.<br>
b. Formát zprávy si můžete zvolit vlastní, ale musí obsahovat minimálně textový
identifikátor senzoru a také hodnotu naměřené teploty (ve °C, s přesností na
desetiny a v rozsahu vhodném pro běžnou domácnost - mimo tento rozsah
musí zprávy zahazovat).<br>
c. Bude číst pouze nejnovější zprávy z Kafky.<br>
d. Na výstupu bude vypisovat aplikace ke každé zprávě unikátní identifikátor
instance aplikace a za ním obsah načtené zprávy.<br>
📂 [py/](https://github.com/AdamLnenicka/ADS2/tree/main/py)

ve složce py/reader
```cmd
docker build -t temperature_reader .
```
ve složce py/producer
```cmd
docker build -t temperature_producer .
```

- Aplikace manifestu

ve složce /k8s/tempr/
```cmd
kubectl apply -f .
```

ve složce /k8s/producer/
```cmd
kubectl apply -f .
```

Pro zjištění identifikátoru instance tempr (temperature_reader):
```cmd
kubectl get pod
```
```cmd
kubectl exec -it {nazev-tempr-podu} -- bash
```
```cmd
python temperature_reader.py
```

6. Zajistěte, aby aplikace temperature_reader běžela v Kubernetu ve dvou instancích.<br>
📂 [k8s/tempr/tempr.yaml](https://github.com/AdamLnenicka/ADS2/blob/main/k8s/tempr/tempr.yaml)
7. Zajistěte, aby parametr “topic” pro temperature_reader byl konfigurovatelný
z Kubernetes.<br>
📂 [k8s/tempr/tempr.yaml](https://github.com/AdamLnenicka/ADS2/blob/main/k8s/tempr/tempr.yaml)<br>
📂 [py/temperature_reader.py](https://github.com/AdamLnenicka/ADS2/blob/main/py/reader/temperature_reader.py)
9. Vyzkoušejte rolling update aplikace temperature_reader.<br>
```cmd
kubectl rollout restart deployment tempr
```

Další příkazy pro hraní si s topicem v kafce:
📝 Popis topicu:
```cmd
kafka-topics.sh --bootstrap-server kafka:9092 --describe --topic temperature
```
🗑️ Smazání topicu:
```cmd
kafka-topics.sh --bootstrap-server kafka:9092 --delete --topic temperature
```
📃 Listnutí všech topiců:
```cmd
kafka-topics.sh --bootstrap-server kafka:9092 --list
```
⚒ Producent pro topic:
```cmd
kafka-console-producer.sh --bootstrap-server kafka:9092 --topic temperature
```

kubectl rollout restart deployment producer
kubectl rollout restart deployment tempr
```

