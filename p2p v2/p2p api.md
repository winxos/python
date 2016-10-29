#p2p client method
>winxos 2015-12-05

##used method
1. Input **nickname** when scripts start.
2. Input **getusers** to get online users.
3. Input **link xxx** to create link with xxx.
4. That's all.

##shake hands

1. Client login first. **connect name pwd**
2. Client send heart packets. **heart nickname**
3. Server remove clients which timeout more than one minute.
4. Client quest online users. **"getusers"**, server return **"server retusers user1 user2 ..."**
5. Once recieved **"server link ip port"**, send **"answer from selfname"** to **ip port**.once recieved **"server retaddr b ip port"**, update clients list of **b** with **"ip port"**
6. Once recieved **"client from xxx"**, update address of xxx in clients list, xxx connected.
7. Once recieved **"answer from xxx"**,  send **"client from selfname"** to xxx.
8. Client create connection with B:
> Send **"client getaddr Bname"** to server, wait recieved Bname's address, then send empty packets to Bname's address, then send **"client link Bname"** to server.
9. That's all.

