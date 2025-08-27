class InMemoryDB:
    def __init__(self):
        self.data = {}
        self.transactions = []

    def _set(self, key, value):
        if self.transactions:
            self.transactions[-1][key] = value
        else:
            self.data[key] = value

    def set(self, key, value):
        self._set(key, value)

    def get(self, key):
        for txn in reversed(self.transactions):
            if key in txn:
                return txn[key]
        return self.data.get(key, None)

    def unset(self, key):
        if self.transactions:
            self.transactions[-1][key] = None
        else:
            self.data.pop(key, None)

    def counts(self, value):
        keys = set(self.data.keys())
        for txn in self.transactions:
            keys.update(txn.keys())
        count = 0
        for key in keys:
            v = self.get(key)
            if v == value:
                count += 1
        return count

    def find(self, value):
        keys = set(self.data.keys())
        for txn in self.transactions:
            keys.update(txn.keys())
        found = []
        for key in keys:
            if self.get(key) == value:
                found.append(key)
        return found

    def begin(self):
        self.transactions.append({})

    def rollback(self):
        if not self.transactions:
            print("NO TRANSACTION")
        else:
            self.transactions.pop()

    def commit(self):
        if not self.transactions:
            print("NO TRANSACTION")
        else:
            changes = self.transactions.pop()
            if self.transactions:
                # Сливаем изменения в родительскую транзакцию
                for key, value in changes.items():
                    self.transactions[-1][key] = value
            else:
                # Если транзакций больше нет, записываем в основную базу
                for key, value in changes.items():
                    if value is None:
                        self.data.pop(key, None)
                    else:
                        self.data[key] = value


def main():
    db = InMemoryDB()
    try:
        while True:
            try:
                line = input("> ").strip()
            except EOFError:
                break
            if not line:
                continue
            parts = line.split()
            cmd = parts[0].upper()
            args = parts[1:]

            if cmd == "END":
                break
            elif cmd == "SET" and len(args) == 2:
                db.set(args[0], args[1])
            elif cmd == "GET" and len(args) == 1:
                val = db.get(args[0])
                print(val if val is not None else "NULL")
            elif cmd == "UNSET" and len(args) == 1:
                db.unset(args[0])
            elif cmd == "COUNTS" and len(args) == 1:
                print(db.counts(args[0]))
            elif cmd == "FIND" and len(args) == 1:
                found = db.find(args[0])
                print(" ".join(found) if found else "NULL")
            elif cmd == "BEGIN":
                db.begin()
            elif cmd == "ROLLBACK":
                db.rollback()
            elif cmd == "COMMIT":
                db.commit()
            else:
                print("UNKNOWN COMMAND")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
