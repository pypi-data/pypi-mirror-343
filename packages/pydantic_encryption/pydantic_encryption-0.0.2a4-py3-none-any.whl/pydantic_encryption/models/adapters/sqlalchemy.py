try:
    from sqlalchemy import func
    from sqlalchemy.dialects.postgresql import BYTEA
    from sqlalchemy.types import TypeDecorator, Text
except ImportError:
    sqlalchemy_available = False
else:
    sqlalchemy_available = True


class PGPSymEncrypted(TypeDecorator):
    """
    A SQLAlchemy type that, on the bind side, wraps INSERT/UPDATE values in
    pgp_sym_encrypt(val, :key) and on the result side wraps the column in
    pgp_sym_decrypt(col, :key)::text
    """

    impl = BYTEA
    cache_ok = True

    def __init__(self, key, *args, **kwargs):
        """
        key: either a literal string or a SQLAlchemy bindparam / text() expression.
        """

        if not sqlalchemy_available:
            raise ImportError(
                "SQLAlchemy is not available. Please install this package with the `sqlalchemy` extra."
            )

        self._key = key
        super().__init__(*args, **kwargs)

    def bind_expression(self, bindvalue):
        # wrap any value we bind with pgp_sym_encrypt(...)
        return func.pgp_sym_encrypt(bindvalue, self._key)

    def column_expression(self, col):
        # whenever we SELECT, automatically decrypt and cast back to text
        return func.pgp_sym_decrypt(col, self._key).cast(Text)

    def copy(self, **kw):
        # ensure key survives copies / caching
        return PGPSymEncrypted(self._key, **kw)
