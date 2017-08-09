.. This file is part of the OpenDSA eTextbook project. See
.. http://algoviz.org/OpenDSA for more details.
.. Copyright (c) 2012-2016 by the OpenDSA Project Contributors, and
.. distributed under an MIT open source license.

.. avmetadata::
   :author: Cliff Shaffer, Mohammed Mostafa, and Margaret Ellis
   :requires: Pointer intro
   :satisfies:
   :topic: Link Nodes

Link Nodes
==========

Link Nodes
----------

In this module, we introduce the idea of a :term:`link node`.
This has some sort of value field, and a pointer to another link
node.
Later, you will learn about :term:`linked lists <linked list>`,
which are made from link nodes.
For now, we will just use them as a simple way to connect some objects
together.

Here is a class definition for a basic link object.
(Need to change this slightly to have better field names: next and
element instead of n and e.)

.. codeinclude:: Lists/Link
   :tag: Link

Here are examples for referencing Link objects in a chain, and getting
at the contents of a link object.

.. TODO::
   :type: Slideshow

   This will implement the first slide from Margaret's powerpoint deck.
   Show a chain of four Link nodes, with the first pointed to by
   "head". (Use the code from the second slideshow here to set it up.)
   Now, show the execution of the following code::

      Link p = head;
      Link q = head.next;
      Link r = q.next;
      Integer myVal = q.element;

How do we set up the chain to begin with?

.. TODO::
   :type: Slideshow

   Show the execution of the following code::

      Link head = new Link(null, null);
      head.element = new Integer(20); // We can set the value of an element field
      head.next = new Link(new Integer(30), null); // We can set the element value directly in the constructor.
                                                   // But we have to store an object, not a primitive.
      head.next.next = new link(new Integer(10), null);
      Link temp = head.next.next; // It can get tiresome to chain all the "next" fields from the head
      temp.next = new link(new Integer(5), null);

One can easily write a loop to iterate through all the Links on a
chain, without needing to know how many there actually are.

.. TODO::
   :type: Slideshow

   This will implement the second slide from Margaret's powerpoint deck.
   Show a chain of four Link nodes (generated in the previous
   slideshow), with the first pointed to by "head"
   Now, show the execution of the following code::

      Link curr = head;
      while (curr.next != null)
        curr = curr.next;

One can remove a Link from a chain.

.. TODO::
   :type: Slideshow

   This will mplement the third slide from Margaret's powerpoint deck.
   Show a chain of four Link nodes (generated by the code of the
   second slideshow here), with the first Link pointed to by "head".
   Now, show the execution of the following code::

      Link q = head.next;
      head.next = q.next;
      q = head.next;

   Note that (eventually) the garbage collector will reclaim the
   dangling node.

Finally, we can also insert new Links.

.. TODO::
   :type: Slideshow

   This will mplement the fourth slide from Margaret's powerpoint deck.
   Show a chain of three Link nodes (the result from the previous
   slideshow here), with the first Link pointed to by "head".
   Now, show the execution of the following code::

      Link newLink = new Link(8, null);
      newLink.next = head;
      head = newLink;

Here is an exercise to practice manipulating link nodes.

.. avembed:: Exercises/Pointers/PointerEX3PRO.html ka