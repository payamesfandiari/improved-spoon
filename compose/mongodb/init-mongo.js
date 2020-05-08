db.createUser(
    {
        user: "mongo",
        pwd: "1qazxsw@",
        roles: [
            {
                role: "readWrite",
                db: "spoon"
            }
        ]
    }
)
