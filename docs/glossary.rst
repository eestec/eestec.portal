Definitions of basic terms
==========================

EESTEC
------

Terms that appear in the general EESTEC context and can help understand context
and use-cases behind the code in ``eestec.portal`` package.

.. glossary::

    Member of EESTEC International
        A member of EESTEC is always an association.

    LC (Local Committee)
        An association the General Assembly of EESTEC has accepted as a full
        member. Must organize international events and has a vote in the General
        Assembly. They can freely apply for all events.

    JLC (Junior Local Committee)
        In this membership level the association must be registered. They have
        an obligation to try to hold an international event within two years or
        they will be demoted. They do not have a vote in General Assembly.
        Promotion to this status is handled by the General Assembly. They can
        freely apply for all events.

    Observer
        In this membership level the association must be organized. They should
        register within two years or they are automatically demoted. They do not
        have a vote in the general assembly. They are promoted to this status by
        the international Board. They can freely apply for all events.

    Observer Candidate
        Any interested party can apply for this status from the international
        Board. They can apply for events with the acceptal of VC-EA.

    Organizer
        An LC that is organizing an event.

    CP (Contact Person)
        The person in an LC which handles communcation between local level and
        international level.

    VC-IA (Vice Chairperson for Internal Affairs)
        The person in the international Board who is responsible for staying
        bidirectionally in touch with EESTEC member organizations (ie. LCs)

    VC-EA (Vice Chairperson for External Affairs)
        The person in the international Board who is responsible for staying in
        contact with partner organizations and expansion of EESTEC.

    International Board
        The board to run practical level tasks. Elected by GA in every Congress.
        The term of the board is from Congress to Congress.

    Local Board
        The board of a member organization (ie. an LC).

    Event
        An event held by a member organization (ie. an LC) into which people
        from other member organizations can apply.

    Event Application Deadline
        Deadline until members of member organizations (ie. LCs) can apply for
        an event.


Technical
---------

Terms that appear in more technical contexts and expect the reader to have
some development background.

.. glossary::

    [Plone Object] EestecMember
        A Plone object representing a single EESTEC member storing his personal
        information.

    [Plone Object] LC
        A Plone object representing a single local committee. Based on it's
        workflow state it is defined whether it is a normal LC, or maybe a JLC
        or Observer. LC is folderish and contains LC specific information such
        as news, events, etc.

    [Plone Object] Event
        A Plone object representing a single EESTEC event, whether it is a
        workshop, exchange, ECM, Congres, etc. It contains all relevant
        information about an event. Event is folderish contains
        EventApplications. Events are contained in LCs.

    [Plone Object] EventApplication
        A Plone object representing a single event application by an EESTEC
        member. It can only be contained within a single Event. EventApplication
        stores a relation to a member and so provides all necessary data about
        the participant.
