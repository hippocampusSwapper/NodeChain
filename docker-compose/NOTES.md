
- Create new wallet
```
bitcoin-cli --rpcuser=swapper --rpcpassword=swapper createwallet testWallet4
```
- Mine blocks for generating BTC
```
bitcoin-cli --rpcuser=swapper --rpcpassword=swapper -generate 200
```
- Send 1 BTC to address bcrt1qjgrlgm57tk0mfan4tnqm2ds8k7dzhw6swpjm5e
```
bitcoin-cli --rpcuser=swapper --rpcpassword=swapper sendtoaddress bcrt1qjgrlgm57tk0mfan4tnqm2ds8k7dzhw6swpjm5e 1
```
- Mine 1 block for validating transaciton
```
bitcoin-cli --rpcuser=swapper --rpcpassword=swapper -generate 1
```

## Ethereum

- Suele arrancar el conectar nginx antes que ganache hay que 
buscar una solución, pero si se relanza manualmente despues de 
que ganache este arrancado todo funciona correctamente.

## Bitcoin

- Como cargar un wallet ya creado ? Ahora genero uno nuevo todo el rato