# mini-payments
Small money-transferring application API

Remember to _docker login_ before trying any **Docker** related operation!

If you have never used a **Docker** based environment before, your first step would be likely to execute the command `docker swarm init`. This will allow your physical computer to act as the manager node of an orquested swarm.

Only then you will be able to execute the main script. Make sure your environmental variables are correct inside the _deployment_script.sh_ file, and then execute it. It will create all the necessary and deploy the API server on the 8000 port.

After that, you will have the application ready to recept any requests!

### Explanation of the different endpoints available through HTTP requests:

- **api/login**: Providing _username_ and _password_ in a POST, it will give return a valid token.
- **api/logout**: It will logout any user refered, if SessionAuthentication was being used.
- **api/users**: A GET will get us informations about our current user. A POST with the adequate parameters and a non already registered email will create a new user. A PATCH will modify our current user as desired.

- **api/accounts**: A GET will get us informations about our current account. An empty post from a user without an **Account** assigned will create an assign one.
- **api/accounts/<pk>**: A GET will let us know about the balance of the user with the PK indicated.

- **api/transfers**: A GET will get us the transaction history that involves our current user. A POST with an _amount_, a _receiver_ **UserProfile** ID and an optional _concept_ will create us a **Transfer** record, and execute the balance changes operations in a transactional way. It does some checks, like that of the _amount_ sent will not leave the sender's account on negative numbers, that the _amount_ sent is not negative, and that the _receiver_ **UserProfile** does indeed exists in the system.
