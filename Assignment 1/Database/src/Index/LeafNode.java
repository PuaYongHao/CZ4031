package Index;

import Storage.Address;
import java.util.ArrayList;

public class LeafNode extends Node {

	private LeafNode next;
	private ArrayList<Address> records;

	// Constructor
	public LeafNode() {
		super();
		next = null;
		setIsLeaf(true);
		records = new ArrayList<Address>();
	}

	// Get next leaf node
	public LeafNode getNext() {
		return next;
	}

	// Set next leaf node
	public void setNext(LeafNode next) {
		this.next = next;
	}

	// Get all records in this leaf node
	public ArrayList<Address> getRecords() {
		return records;
	}

	// Get record at given index in this leaf node
	public Address getRecordAtIndex(int index) {
		return records.get(index);
	}

	// Add record
	public int addRecord(int key, Address address) {
		// Assume keys and records are always tally
		int i;
		// Add key to the node
		i = this.addKey(key);
		// Store the record at corresponding index
		// Able to handle i = 0 and i = size-1
		records.add(i, address);

		return i;
	}

	// Delete a record at given index from leaf node
	public void deleteRecordAtIndex(int index) {
		// Make sure keys and records are always tally
		deleteKeyAtIndex(index);
		records.remove(index);
	}

	// Delete all records from leaf node
	public void deleteRecords() {
		// Make sure keys and records are always tally
		deleteKeys();
		records = new ArrayList<Address>();
	}

	@Override
	// Find the smallest key in leaf node
	public int findSmallestKey() {
		int key;
		key = this.getKeyAtIndex(0);
		return key;
	}

	// Delete current leaf node
	public void deleteNode() {
		super.deleteNode();
		this.records = new ArrayList<Address>();
		this.next = null;
	}

}
