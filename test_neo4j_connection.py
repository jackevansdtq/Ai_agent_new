#!/usr/bin/env python3
"""Test Neo4J connection"""
from neo4j import GraphDatabase
import os

NEO4J_URI = os.environ.get('NEO4J_URI', 'neo4j://35.185.131.185:7687')
NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'Khongmanh@2001@')

try:
    print(f"🔌 Connecting to Neo4J: {NEO4J_URI}")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    
    with driver.session() as session:
        # Test connection
        result = session.run("RETURN 1 as test")
        print("✅ Neo4J connection successful!")
        
        # Count nodes
        result = session.run("MATCH (n) RETURN count(n) as count")
        node_count = result.single()['count']
        print(f"📊 Total nodes in database: {node_count}")
        
        # Count relationships
        result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
        rel_count = result.single()['count']
        print(f"🔗 Total relationships: {rel_count}")
        
        # Check if there are any entities
        result = session.run("MATCH (n:Entity) RETURN count(n) as count")
        entity_count = result.single()['count']
        print(f"📝 Total entities: {entity_count}")
        
    driver.close()
except Exception as e:
    print(f"❌ Neo4J connection error: {e}")
    import traceback
    traceback.print_exc()

