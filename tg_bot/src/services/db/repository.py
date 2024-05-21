from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import text

from services.db.db import async_session_maker

class SQLRepository:
    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session


    async def _execute_stmt(self, stmt):
        async with self.session() as session:
            return await session.execute(stmt)

    # Category methods
    async def get_categories(self, offset=0, limit=10) -> list[tuple]:
        stmt = text("SELECT id, title FROM admin_panel_category LIMIT :limit OFFSET :offset").bindparams(limit=limit, offset=offset)
        return (await self._execute_stmt(stmt)).all()


    async def get_subcategories_from_categories(self, category_id: int, offset=0, limit=10) -> list[tuple]:
        stmt = text("SELECT id, title FROM admin_panel_subcategory WHERE category_id=:category_id LIMIT :limit OFFSET :offset").bindparams(category_id=category_id, limit=limit, offset=offset)
        return (await self._execute_stmt(stmt)).all()
        

    async def get_products_in_subcategories(self, subcategory_id: int, offset=0, limit=10) -> list[tuple]:
        stmt = text("SELECT id, title FROM admin_panel_product WHERE subcategory_id=:subcategory_id LIMIT :limit OFFSET :offset").bindparams(subcategory_id=subcategory_id, limit=limit, offset=offset)
        return (await self._execute_stmt(stmt)).all()


    async def get_product(self, product_id: int) -> tuple:
        stmt = text("SELECT title, description, price, image, amount FROM admin_panel_product WHERE id=:product_id").bindparams(product_id=product_id)
        return (await self._execute_stmt(stmt)).one()


    # Basket methods
    async def add_product_in_basket(self, user_id: int, product_id: int, quantity: int) -> None:
        stmt = text("INSERT INTO admin_panel_productinbasket(basket_id, product_id, quantity) VALUES(:user_id, :product_id, :quantity)").bindparams(user_id=user_id, product_id=product_id, quantity=quantity)
        return await self._execute_stmt(stmt)


    async def get_products_from_basket(self, user_id: int, offset: int=0, limit: int=10) -> list[tuple]:
        stmt = text(
            '''
            SELECT p.id, p.title, pib.quantity
            FROM admin_panel_productinbasket pib
            INNER JOIN admin_panel_product p ON pib.basket_id =:user_id and p.id = pib.product_id
            LIMIT :limit
            OFFSET :offset
            '''
        ).bindparams(user_id=user_id, limit=limit, offset=offset)
        return (await self._execute_stmt(stmt)).all()


    async def delete_backet(self, user_id: int) -> None:
        stmt = text("DELETE FROM admin_panel_basket WHERE user_id=:user_id").bindparams(user_id=user_id)
        return await self._execute_stmt(stmt)
    
    async def sum_basket(self, user_id: int):
        stmt = text('''
                    SELECT SUM(pib.quantity * p.price)
                    FROM admin_panel_productinbasket pib
                    INNER JOIN admin_panel_product p ON pib.basket_id =:user_id and p.id = pib.product_id
                    ''').bindparams(user_id=user_id)
        return (await self._execute_stmt(stmt)).one()
    
    async def get_product_from_basket(self, user_id: int, product_id: int):
        stmt = text('''
                    SELECT quantity
                    FROM admin_panel_productinbasket 
                    WHERE product_id=:product_id AND basket_id=:user_id
                    ''').bindparams(product_id=product_id, user_id=user_id)
        return (await self._execute_stmt(stmt)).one_or_none()
    

    async def create_basket_if_not_exist(self, user_id: int):
        stmt = text('''
                    INSERT INTO admin_panel_basket(user_id)
                    SELECT :user_id
                    WHERE
                        NOT EXISTS (
                            SELECT :user_id FROM admin_panel_basket WHERE user_id =:user_id
                        )
                    ''').bindparams(user_id=user_id)
        return await self._execute_stmt(stmt)


    async def add_product_in_backet(self, user_id: int, product_id: int):
        stmt = text('''
                    INSERT INTO admin_panel_productinbasket(basket_id, product_id, quantity)
                    VALUES(:basket_id, :product_id, 1)
                    ''').bindparams(basket_id=user_id, product_id=product_id)
        return await self._execute_stmt(stmt)
    

    async def update_quantity(self, user_id: int, product_id: int, quantity: int):
        stmt = text('''
                    UPDATE admin_panel_productinbasket
                    SET quantity=:quantity
                    WHERE user_id=:user_id AND product_id=:product_id
                    ''').bindparams(user_id=user_id, product_id=product_id, quantity=quantity)
        return await self._execute_stmt(stmt)

    
    

repository = SQLRepository(async_session_maker)
