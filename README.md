## Running the Services Locally

To start all services, run:
```bash
chmod +x start-services.sh
./start-services.sh
```

To stop all services, use Ctrl + C, then run:
```bash
chmod +x stop-services.sh
./stop-services.sh
```


## Running Frontend locally:
1. Create a folder
2. navigate to the folder
3. sudo git clone https://github.com/julianroloff/VibeMap.git
4. cd VibeMap/frontend/quasar-project
5. sudo npm install quasar
6. sudo quasar dev -m pwa --host
