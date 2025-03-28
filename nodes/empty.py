from langgraph.graph import StateGraph, START, END
from config.states import MessagesState
from config.config import logger


def empty_func(state: MessagesState):
    """
    literally an empty function
    """
    logger.info("In empty function")
    description = ("""Online Flower Shop Project Description

1. Target Audience:
   - Individuals looking for personal floral gifts and home decor.
   - Businesses and event planners needing floral arrangements for events, offices, and special occasions.

2. Product Range:
   - Fresh flower bouquets categorized by occasion (e.g., birthdays, anniversaries, sympathy).
   - Potted plants and succulents for home and office decor.
   - Custom floral arrangements for weddings, corporate events, and other special occasions.
   - Gift items such as chocolates, greeting cards, and vases.

3. Delivery Options:
   - Local delivery within a specified region with options for same-day and next-day delivery.
   - Scheduled delivery for special events and bulk orders.

4. Payment Methods:
   - Accept major credit/debit cards, PayPal, and other popular online payment systems.
   - Option for gift cards and promotional codes.

5. Website Features:
   - User-friendly interface with high-quality images and detailed product descriptions.
   - User accounts for easy order tracking, wish lists, and personalized recommendations.
   - Order tracking system to keep customers informed about their delivery status.
   - Customer reviews and ratings to build trust and community engagement.
   - Blog section with floral care tips, design inspiration, and seasonal highlights.

6. Design and Branding:
   - Elegant and modern design with a focus on nature-inspired aesthetics.
   - Branding that emphasizes freshness, quality, sustainability, and customer satisfaction.
   - Eco-friendly packaging options to appeal to environmentally conscious consumers.

7. Competitors:
   - Analysis of local and online competitors to identify unique selling points.
   - Differentiation through exclusive floral designs, personalized customer service, and eco-friendly practices.""")

    return {"product_description": description}
    # return None


# Build graph
builder = StateGraph(MessagesState)

# Nodes
builder.add_node("empty_node", empty_func)

# Edges
builder.add_edge(START, "empty_node")
builder.add_edge("empty_node", END)

# Compile
empty_graph = builder.compile()
