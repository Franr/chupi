class RedisKeyMixin:
    @property
    def redis_key(self) -> str:
        """
        Generate a unique key based on the db table name and the primary key.

        :return: a unique key
        """
        key = f"{self._meta.db_table}:{self.pk}"
        return key
